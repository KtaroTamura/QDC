import matplotlib.pyplot  as plt
import numpy as np
import MinuitFit as MiF

def fitfunc_pse(x,a,b,C):
	y=C*pow(10,-a*x/20.)+b
	return y

def fitfunc_thin(x,a,b,C):
	#y=3650*pow(10,-a*x/20.)/pow(10,-4./20)+b
	#y=C*pow(10,-a*x/20.)/pow(10,-4./20.)+b
	y=C*pow(10,-a*x/20.)+b
	return y

def calc_amp(A,dA,B,dB):
	amp=A/B
	damp=np.sqrt((dA/B)**2+(A/(B*B)*dB)**2)
	print("amp={},damp={}".format(amp,damp))
	return amp,damp

if __name__=='__main__':
	data_thick=np.loadtxt("Linearity_thick.csv",delimiter=',',skiprows=0)
	thick=np.array([0.,1.,2.,3.,4.,5.,6.,7.,8.,9.,10.,11.,12.,16.])
	EP_thick=data_thick[:,1]
	EP_thick_err=data_thick[:,2]

	data_thin=np.loadtxt("Linearity_thin.csv",delimiter=',',skiprows=0)
	thin=np.array([4.,5.,6.,7.,8.,9.,10.,11.,12.,16.])
	EP_thin=data_thin[:,1]
	EP_thin_err=data_thin[:,2]

	ax=plt.subplot()
	plt.errorbar(thick,EP_thick,yerr=EP_thick_err,fmt='o',label='thick',color='b')
	plt.errorbar(thin,EP_thin,yerr=EP_thin_err,fmt='o',label='thin',color='r')
	MiF.Setup(thick,EP_thick,0,EP_thick_err,fitfunc_pse,ax)
#	MiF.SetRange(0,12)
	result1=MiF.chisquare(0.1,1000.,4000)
	zero1=result1[4]+result1[2]
	dzero1=np.sqrt(result1[5]**2+result1[3]**2+(result1[4]*(-1*result1[0]/20)*np.log(10)*result1[1])**2)


	MiF.Setup(thin,EP_thin,0,EP_thin_err,fitfunc_thin,ax)
	result2=MiF.chisquare(0.1,1000.,4000)
	zero2=result2[4]+result2[2]
	dzero2=np.sqrt(result2[5]**2+result2[3]**2+(result2[4]*(-1*result2[0]/20)*np.log(10)*result2[1])**2)
	print("zero2={}+-{}".format(zero2,dzero2))
	amp1,damp1=calc_amp(EP_thick[0],EP_thick_err[0],EP_thick[4],EP_thick_err[4])
	#amp2=calc_amp(zero1,dzero1,EP_thick[4],EP_thick_err[4])
	amp3,damp3=calc_amp(zero2,dzero2,EP_thin[0],EP_thin_err[0])
	ave_amp=(amp1+amp3)/2
	sigma_amp=np.sqrt((damp1**2+damp3**2)/4)
	print("amp={}+-{}".format(ave_amp,sigma_amp))
	plt.title("Attenuator Linearity")
	plt.xlabel(u'Attenuate [-db]')
	plt.ylabel(u'Channel')
	plt.ylim([0,4096])
	plt.legend(bbox_to_anchor=(1,0.7),loc='right')
	plt.show(block=False)
