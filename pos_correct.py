import numpy as np
import math 
import matplotlib.pyplot as plt

sigma=20.
center=33.75

def gauss(x):
	dx=x-center
	y=1/(np.sqrt(2*math.pi)*sigma)*np.exp(-1*dx*dx/(2*sigma*sigma))
	return y

def position(x):
	a=2.0779e-02
	b=1.2468e+03
	C=3.4537e+03
	y=(C*np.exp(-a*x)+b)/2970.
	return y

if __name__=='__main__':
	EP=0
	int_g=0
	x=np.arange(0.,61.75,0.05)
	y=gauss(x)
	z=position(x)
	w=y*z
	plt.plot(x,y,color='r')
	#plt.plot(x,z,color='g')
	plt.plot(x,w,color='b')
	plt.show(block=False)
'''
	for X in range(0,650):
		x=0.1*X
		g=gauss(x)
		y=gauss(x)*position(x)
		EP=EP+y
		int_g=int_g+g
		print("EP={},total={}".format(EP,int_g))	
	print("EP={},total={}".format(EP,int_g))
'''
