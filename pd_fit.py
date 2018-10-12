import numpy as np
import MinuitFit as MiF
import matplotlib.pyplot as plt

def func(x,*par):
	a=par[0]
	b=par[1]
	C=par[2]
	y=C*np.exp(-1.*a*x)+b
	return y

#def MiF_Setup(data_x,data_y,xerr,yerr,**par,)

if __name__=='__main__':
	position=np.array([5.75,19.75,33.75,47.75,61.75])
	EP=np.array([4280.,3600.,2970.,2430.,2260.])
	n=EP.shape[0]
	p_err=np.full(n,1.)
	err=np.full(n,100.)
	ax=plt.subplot()
	ax.errorbar(position,EP,xerr=p_err,yerr=err,fmt='o',color='b')
	MiF.Setup(position,EP,p_err,err,func,ax)
	MiF.SetRange(0.,35.)
#	X,Y,Xe,Ye=MiF.SetRange(0.,35.)
#	l=MiF.im.Minuit(MiF.least_square3,a=0.02,b=1000,c=1000,error_a=0.1,error_b=0.1,error_c=0.1,limit_a=(0.02,0.03),limit_b=(1000,1300),errordef=1)
#	kkk,param=l.migrad()
	result=MiF.chisquare(0.01,1000,3000.)
	a=result[0]
	b=result[2]
	c=result[4]
#	a=param[0].value
#	b=param[1].value
#	c=param[2].value
	fit_result=func(position,a,b,c)
	#plt.plot(position,fit_result,color='r')
#	MiF.ppap()
	plt.show(block=False)
