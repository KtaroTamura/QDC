import matplotlib.pyplot  as plt
import numpy as np
import MinuitFit as MiF

def fitfunc_pse(x,a,b):
	y=3720*pow(10,-a*x/20.)+b
	return y

def fitfunc_source(x,a,b):
	y=3700*pow(10,-a*x/20.)/pow(10,-4./20)+b
	return y

if __name__=='__main__':
	Att_pse=np.array([0.,1.,2,3,4,5,6,7,8,9,10,11,12,16])
	channel_pse=np.array([3720.,3300,2940,2610,2280,2020,1770,1570,1370,1210,1050,920,800,440])
	channel_pse_err=np.array([130,110,110,105,80,75,60,55,50,45,35,35,25,40])
	#channel_pse_err=np.full(Att_pse.shape[0],20.)

	Att_source=np.array([4.,5,6,7,8,10,15,20])
	channel_source=np.array([3700.,3300,2950,2600,2150,1600,800,300])
	channel_source_err=np.array([100,100,100,100,100,100,100,100])

	ax=plt.subplot()
	plt.errorbar(Att_pse,channel_pse,yerr=channel_pse_err,fmt='o',label='pseude analog',color='b')
	plt.errorbar(Att_source,channel_source,yerr=channel_source_err,fmt='o',label='source',color='r')
	MiF.Setup(Att_pse,channel_pse,0,channel_pse_err,fitfunc_pse,ax)
	result1=MiF.chisquare(0.1,1000.)
	#result1=MiF.chisquare(0.1,1000.)

	MiF.Setup(Att_source,channel_source,0,channel_source_err,fitfunc_source,ax)
	result2=MiF.chisquare(0.1,1000.,Dopt=False)
	plt.title("Attenuator Linearity")
	plt.xlabel(u'Attenuate [-db]')
	plt.ylabel(u'Channel')
	plt.ylim([0,4096])
#	plt.legend(loc='upper right')
	plt.show(block=False)
