import myfunc as mf
import numpy as np
import sys,re
import matplotlib.pyplot as plt

dCH=3.787765e-02
##Myfunc setup##
#define inside depth
mf.depth_Al=0.02
mf.depth_CH=0.1124
mf.depth_Pb=0.01
mf.sigma=0.01257

if __name__=='__main__':
	##Initialize##
	T0=np.array([])
	T1=np.array([])
	Tout=np.array([])
	Pori=np.array([])
	Pout=np.array([])
	Pin=np.array([])
	flag=0
	##Calc Ori&Out##
	for e in range(1,2281):
		T=0.001*e
		T2=mf.int_bethe(T)
		T0=np.append(T0,T)
		T1=np.append(T1,T2)
		P1=mf.Fermi(T)*mf.calc(T)
		Pori=np.append(Pori,P1)
		if T2>0:
			if flag==0:
				flag+=1
			Pin=np.append(Pin,P1)
		else:
			Pin=np.append(Pin,0)	

	##Redefinition depth##
	mf.depth_Al=0.03
	mf.depth_CH=0.15
	mf.depth_Pb=0.01
	mf.sigma=0.01257

	for e in range(1,2281):
		T=0.001*e
		T2=mf.int_bethe(T)
		Tout=np.append(Tout,T2)
		P1=mf.Fermi(T)*mf.calc(T)
		if T2>0:
			Pout=np.append(Pout,P1)
		else:
			Pout=np.append(Pout,0)

	##Nornalize##
	Pori=Pori/Pori.sum()
	Pin=Pin/Pin.sum()
	Pout=Pout/Pout.sum()

	##DrawGrpah##
	plt.plot(T0,Pori,color='b',label='original')
	plt.plot(Tout,Pout,color='r',label='outside')
	plt.plot(T1,Pin,color='g',label='inside')
	plt.legend(loc='upper right')
	plt.title('Simulation of Y90 Spectrum')	
	plt.xlabel('Energy[MeV]')	
	plt.ylabel('Distribution')
	plt.xlim([0,None])
	plt.ylim([1e-8,None])
	plt.yscale('log')	
	plt.show(block=False)
	
