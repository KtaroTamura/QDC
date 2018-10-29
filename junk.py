import matplotlib.pyplot  as plt
import numpy as np
import MinuitFit as MiF

def fitfunc_pse(x,a,b,C):
	return y


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
	plt.scatter(EP_thick,EP_thick_err,label='thick',color='b')
	plt.scatter(EP_thin,EP_thin_err,label='thin',color='r')
	plt.title("Attenuator Linearity")
	plt.xlabel(u'Attenuate [-db]')
	plt.ylabel(u'Channel')
	plt.ylim([0,100])
	plt.legend(bbox_to_anchor=(1,0.7),loc='right')
	plt.show(block=False)
