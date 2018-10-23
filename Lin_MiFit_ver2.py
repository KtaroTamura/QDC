import matplotlib.pyplot  as plt
import numpy as np
import MinuitFit as MiF

def fitfunc_pse(x,a,b,C):
	y=C*pow(10,-a*x/20.)+b
	return y

def fitfunc_thin(x,a,b,C):
	#y=3650*pow(10,-a*x/20.)/pow(10,-4./20)+b
	y=C*pow(10,-a*x/20.)+b
	return y

if __name__=='__main__':
	thick=np.array([0.,1.,2.,3.,4.,5.,6.,7.,8.,9.,10.,11.,12.,16.])
	EP_thick=np.array([3720.,3300,2940,2610,2280,2020,1770,1570,1370,1210,1050,920,800,440])
	EP_thick_err=np.array([130,110,110,105,80,75,60,55,50,45,35,35,25,40])
	#EP_thick_err=np.full(thick.shape[0],20.)

	thin=np.array([4.,5.,6.,7.,8.,9.,10.,11.,12.])
	EP_thin=np.array([3650,3180,2765,2395,2060,1770,1515,1290,1085])
	EP_thin_err=np.full(thin.shape[0],20)

	ax=plt.subplot()
	plt.errorbar(thick,EP_thick,yerr=EP_thick_err,fmt='o',label='pseude analog',color='b')
	plt.errorbar(thin,EP_thin,yerr=EP_thin_err,fmt='o',label='source',color='r')
	MiF.Setup(thick,EP_thick,0,EP_thick_err,fitfunc_pse,ax)
	result1=MiF.chisquare(0.1,1000.,4000)

	MiF.Setup(thin,EP_thin,0,EP_thin_err,fitfunc_thin,ax)
	MiF.SetRange(0,10.)
	result2=MiF.chisquare(0.1,1000.,4000)
	plt.title("Attenuator Linearity")
	plt.xlabel(u'Attenuate [-db]')
	plt.ylabel(u'Channel')
	plt.ylim([0,4096])
#	plt.legend(loc='upper right')
	plt.show(block=False)
