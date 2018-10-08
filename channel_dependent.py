import matplotlib.pyplot  as plt
import numpy as np
import scipy.optimize

def fitfunc(x,a,b,C):
	y=C*np.exp(-1*a*x)+b
	return y

if __name__=='__main__':
	position=np.array([5.75,19.75,33.75,47.75,61.75])
	EP=np.array([4280.,3600.,2970.,2430.,2260.])

	plt.scatter(position,EP,label='channel izon',color='b')
	para_init=np.array([1.,0,4280.])
	para_opt, conv=scipy.optimize.curve_fit(fitfunc,position,EP,para_init)
	print("pseude",para_opt)
	fit_result=fitfunc(position,para_opt[0],para_opt[1],para_opt[2])
	plt.plot(position,fit_result,label='fit',color='r')
	plt.title("Attenuator Linearity")
	plt.xlabel(u'Channel')
	plt.ylabel(u'End point')
	plt.ylim([0,4500])
	plt.legend(loc='upper right')
	plt.show(block=False)
