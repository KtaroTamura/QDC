import numpy as np
import matplotlib.pyplot as plt
import MinuitFit as MiF

def func(x,*par):
	a=par[0]
	b=par[1]
	c=par[2]
	y=c*np.exp(-1*a*x)+b
	return y

if __name__=='__main__':
	pos=np.array([5.75,19.75,33.75,47.75,61.75])
	time=np.array([61524,60552,64438,63065,60213])
	count=np.array([4279175,3948669,3826957,3458695,3016914])
	time=time/1000
	pos_err=np.full(pos.shape[0],1.)
	rate=count/time
	rate_err=np.sqrt(rate)
	ax=plt.subplot()
	ax.errorbar(pos,rate,xerr=pos_err,yerr=rate_err,fmt='o',color='b')
	MiF.Setup(pos,rate,pos_err,rate_err,func,ax)
	MiF.SetLimit(lim_a=(0,5),lim_b=(0,None))
	result=MiF.chisquare(-10,10000,100000)
	plt.title('count rate vs source position')
	plt.xlabel('Source position (from down)')
	plt.ylabel('rate')
	plt.ylim([0,100000])
	plt.show(block=False)
