from scipy.special import gamma
import ROOT,sys,csv
import math 
from libc.math cimport log,sqrt,pow,log10

E_max=2.28
##Spectrum Constant##
cdef:
	float alpha=0.007287
	float Z=40
	float A=90
	float hc=197.
	float me=0.511

##Bethe-Bloch Aluminium Constant##
cdef:
	float bethe_const=0.1535
	float ZAl=13
	float AAl=27
	float I_Al=163*pow(10,-6)
	float c=2.998*pow(10,8)
	float n_Al=2.7
	float C_parAl=-4.24
	float a_parAl=0.0802
	float m_parAl=3.63
	float X0_parAl=0.1708
	float X1_parAl=3.01
depth_Al=0.01

##Bethe-Bloch Lead Constant##
cdef:
	float ZPb=82
	float APb=208
	float I_Pb=823*pow(10,-6)
	float n_Pb=11.34
	float C_parPb=-6.20
	float a_parPb=0.0936
	float m_parPb=3.16
	float X0_parPb=0.3776
	float X1_parPb=3.81
depth_Pb=0.01

##Bethe-Bloch plastic Constant##
cdef:
	float ZA_C=6/12
	float ZA_H=1/1
	float I_CH=64.7*pow(10,-6)
	float n_CH=1.032
	float C_parCH=-3.20
	float a_parCH=0.1610
	float m_parCH=3.24
	float X0_parCH=0.1464
	float X1_parCH=2.49
depth_CH=0.01

##Gauss Set Up##
sigma=0.3

##Spectrum  Calclator##
cpdef double Fermi(double T):
	cdef double R,g,p,v,part1,part2,part3,part4,F
	R=1.25*pow(A,0.33)/hc
	g=sqrt(1-alpha*alpha*Z*Z)
	p=sqrt(T*T+2*me*T)
	v=alpha*Z*(T+me)/p
	part1=((1+g)/2)*4*pow(2*p*R,2*g-2)
	part2=math.exp(+math.pi*v)
	part3=abs(gamma(g+1j*v))
	part4=gamma(2*g+1)
	F=part1*part2*part3*part3/(part4*part4)
	return F

cpdef double calc(double T):
	cal=(E_max-T)*(E_max-T)*(T+me)*sqrt(T*T+2*me*T)
	return cal

##Bethe-Bloch##
cdef double bethe(double T,int mat):
	cdef double beta,gam,eta,W_max,X_par
	beta=sqrt(1-me/(T+me)*(me/(T+me)))
	gam=1/sqrt(1-beta*beta)
	eta=beta*gam
	W_max=2*me*eta*eta/(1+2*sqrt(1+eta*eta)+1)
	X_par=log10(eta)
	if mat==1:
		logpart=log(2*me*beta*beta*gam*gam*W_max/(I_Al*I_Al))
		if X_par<X0_parAl:
			delta=0
		elif X_par>X0_parAl and X_par<X1_parAl:
			delta=4.6052*X_par+C_parAl+a_parAl*pow(X1_parAl-X_par,m_parAl)
		elif X_par>X1_parAl:
			delta=4.6052*X_par+C_parAl+a_parAl
		return bethe_const*ZAl/AAl/(beta*beta)*(logpart-2*beta*beta-delta)*n_Al*depth_Al
	elif mat==2:
		logpart=log(2*me*beta*beta*gam*gam*W_max/(I_CH*I_CH))
		if X_par<X0_parCH:
			delta=0
		elif X_par>X0_parCH and X_par<X1_parCH:
			delta=4.6052*X_par+C_parCH+a_parCH*pow(X1_parCH-X_par,m_parCH)
		elif X_par>X1_parCH:
			delta=4.6052*X_par+C_parCH+a_parCH
		original=bethe_const/(beta*beta)*(logpart-2*beta*beta-delta)
		return (9*12*ZA_C+10*1*ZA_H)/118*original*n_CH*depth_CH
	elif mat==3:
		logpart=log(2*me*beta*beta*gam*gam*W_max/(I_Pb*I_Pb))
		if X_par<X0_parPb:
			delta=0
		elif X_par>X0_parPb and X_par<X1_parPb:
			delta=4.6052*X_par+C_parPb+a_parPb*pow(X1_parPb-X_par,m_parPb)
		elif X_par>X1_parPb:
			delta=4.6052*X_par+C_parPb+a_parPb
		original=bethe_const/(beta*beta)*(logpart-2*beta*beta-delta)
		return bethe_const*ZPb/APb/(beta*beta)*(logpart-2*beta*beta-delta)*n_Pb*depth_Pb
	
##integral_bethe##
cdef double int_bethe(double T):
	cdef:
		int l
		double T0,Eloss
	T0=T
	for l in range(0,10):
		Eloss=(bethe(T0,1)+bethe(T0,2)+bethe(T0,3))*0.1
		T0=T0-Eloss
		if T0<5e-04:
			T0=0
			break
	return T0

##E_correction##
def E_correction(double E_det):
	cdef int L
	cdef double delta,loss,E_emit,M
	delta=0.6
	pre_delta=0.5
	E_emit=0
	for L in range(1,100):
		loss=0.01*L
		if E_det+loss>0:
			M=(E_det+loss)-int_bethe(E_det+loss)
			delta=abs(M-loss)
			#print(pre_delta)
			if delta<pre_delta:
				pre_delta=delta
				E_emit=E_det+loss
			elif delta<0.001:
				pre_delta=delta
				E_emit=E_det+loss
				break
	return E_emit

##Gaussian correction##
cdef double Gauss(double x):
	cdef double f
	f=1/(sqrt(2*math.pi*sigma*sigma))*math.exp(-x*x/(sigma*sigma))
	return f

def G_correction(double T):
	cdef int X
	cdef double x,P,g_list,g_average
	g_list=0
	w=0
	for X in range(-5,6):
		w=w+1
		x=X*0.05
		f=Gauss(x)
		if T+x>0 and T+x<E_max:
			P=Fermi(T+x)*calc(T+x)*f
		else:
			P=Fermi(T)*calc(T)*f
		g_list=g_list+P
	g_average=g_list/w
	return g_average

