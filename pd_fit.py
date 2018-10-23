import numpy as np
import MinuitFit as MiF
import matplotlib.pyplot as plt

def func(x,*par):
	a=par[0]
	b=par[1]
	C=par[2]
	y=C*np.exp(-1.*a*x)+b
	return y


if __name__=='__main__':
	position=np.array([5.75,19.75,33.75,47.75,61.75])
	EP=np.array([4280.,3600.,2970.,2430.,2260.])
	n=EP.shape[0]
	p_err=np.full(n,1.)
	err=np.full(n,100.0)
	ax=plt.subplot()
	ax.errorbar(position,EP,xerr=p_err,yerr=err,fmt='o',color='b',label='experiment')
	MiF.Setup(position,EP,p_err,err,func,ax)
#	MiF.SetRange(0.,35.)
	MiF.SetLimit(lim_a=(0,1),lim_b=(500,1500))
	result=MiF.chisquare(0.01,1000,3000)
	plt.title(u'SC position dependent')
	plt.xlabel(u'source position (from down)')
	plt.ylabel(u'End point')
	plt.ylim([0,4500])
	plt.show(block=False)
