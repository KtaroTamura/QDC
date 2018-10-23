import matplotlib.pyplot  as plt
import numpy as np
import MinuitFit as MiF

def fitfunc_pse(x,a,b):
	y=a*x+b
	return y


if __name__=='__main__':
	Att_pse=np.array([0.,1.,2,3,4,5,6,7,8,9,10,11,12,16])
	channel_pse=np.array([3720.,3300,2940,2610,2280,2020,1770,1570,1370,1210,1050,920,800,440])
	channel_pse_err=np.array([130,110,110,105,80,75,60,55,50,45,35,35,25,40])
	err_err=np.full(Att_pse.shape[0],10.)

	ax=plt.subplot()
	MiF.Setup(channel_pse,channel_pse_err,channel_pse,err_err,fitfunc_pse,ax)
	MiF.SetRange(700,3800)
	result=MiF.chisquare(1,0.)
	plt.errorbar(channel_pse,channel_pse_err,xerr=channel_pse_err,yerr=err_err,fmt='o',label='pseude analog',color='b')
	plt.title("Error Linearity")
	plt.xlabel(u'EP')
	plt.ylabel(u'Error')
	plt.xlim([0,4000])
	plt.ylim([0,150])
	#plt.legend(loc='upper right')
	plt.show(block=False)
