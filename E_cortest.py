import myfunc as mf
import matplotlib.pyplot as plt
import numpy as np
mf.depth_Al=0.01
mf.depth_CH=0.03963
mf.depth_Pb=0.008

if __name__=='__main__':
	T_array=np.array([])
	T0_array=np.array([])
	y_array=np.array([])
	for i in range(1,230):
		T0=0.01*i
		T=mf.int_bethe(T0)
		y=mf.E_correction(T0)
		#y=mf.E_correction(T)-T
		#y=mf.int_bethe(T)
		T_array=np.append(T_array,T0)	
		y_array=np.append(y_array,T)	
	plt.plot(T_array,y_array)
	plt.xlabel('E_det')
	plt.ylabel('E_emit')
	plt.show(block=False)
	

