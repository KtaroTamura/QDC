import numpy as np
import iminuit as im
import matplotlib.pyplot as plt

##index##
'''
Setup(x,y,xerr,yerr,func,ax)

chisquare(*par)
	least_square1~4()
	|	fitfunc()
	|	project_err()
	|
	Draw_graph()

SetRange()
'''
sigma=0.1

def Setup(main_x,main_y,main_xerr,main_yerr,main_func,main_ax):
	global data_x
	global data_y
	global x_err
	global y_err
	global fitfunc
	global ax
	global xmin
	global xmax
	global x_div
	data_x=main_x
	data_y=main_y
	x_err=main_xerr
	y_err=main_yerr
	fitfunc=main_func
	ax=main_ax
	xmin=np.amin(data_x)
	xmax=np.amax(data_x)
	x_div=(xmax-xmin)/100
	return 0

def chisquare(*par):
	par_num=len(par)
	if par_num==1:
		m=im.Minuit(least_square1,a=par[0],error_a=0.1,errordef=1)
	elif par_num==2:
		m=im.Minuit(least_square2,a=par[0],b=par[1],error_a=0.1,error_b=0.1,errordef=1)
	elif par_num==3:
		m=im.Minuit(least_square3,a=par[0],b=par[1],c=par[2],error_a=0.1,error_b=0.1,error_c=0.1,errordef=1)
	elif par_num==4:
		m=im.Minuit(least_square4,a=par[0],b=par[1],c=par[2],d=par[3],error_a=0.1,error_b=0.1,error_c=0.1,error_d=0.1,errordef=1)
	fmin,param=m.migrad()
	res_text=''
	output=[]
	graph_par=[]
	chi=fmin.fval/(len(data_y)-2)
	for ii in range(0,par_num):
		output.extend([param[ii].value,param[ii].error])
		graph_par.extend([param[ii].value])
		onestr='par{}= {} +- {}'.format(ii,param[ii].value,param[ii].error)+'\n'
		res_text=res_text+onestr
	output.append(chi)
	res_text=res_text+'chi2/ndf={}'.format(chi)
	Draw_graph(*graph_par,k=chi)
	print(res_text)
	print('**************************************************\n\n')
	return output 


def least_square1(a):
	para=[a]
	vir_err=project_err(*para)
	sigma=y_err**2+vir_err**2
	return sum((data_y-fitfunc(data_x,*para))**2/sigma)

def least_square2(a,b):
	para=[a,b]
	vir_err=project_err(*para)
	sigma=y_err**2+vir_err**2
	return sum((data_y-fitfunc(data_x,*para))**2/sigma)

def least_square3(a,b,c):
	para=[a,b,c]
	vir_err=project_err(*para)
	sigma=y_err**2+vir_err**2
	return sum((data_y-fitfunc(data_x,*para))**2/sigma)

def least_square4(a,b,c,d):
	para=[a,b,c,d]
	vir_err=project_err(*para)
	sigma=y_err**2+vir_err**2
	return sum((data_y-fitfunc(data_x,*para))**2/sigma)


def Draw_graph(*para,k=0):
	gx=np.empty((0,1))
	for j in range(0,100):
		x=xmin+j*x_div
		gx=np.append(gx,x)
	fit_line=fitfunc(gx,*para)
	ax.plot(gx,fit_line,color='r')
	textstr=r'$\chi^2=%.2f$' % (k, )
	par_num=len(para)
	for i in range(0,par_num):
		one='\n'+r'$par{}={:.4E}$'.format(i,para[i])
		textstr=textstr+one
	props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
	plt.text(0.7,0.95,textstr,transform=ax.transAxes,fontsize=14,verticalalignment='top', bbox=props)
	return 0

#
def project_err(*para):
	dh=0.001
	diff=(fitfunc(data_x+dh,*para)-fitfunc(data_x,*para))/dh
	vir_err=diff*x_err
	return vir_err

def fitfunc():
	return 0

def SetRange(x_min,x_max):
	global data_x
	global data_y
	global x_err
	global y_err
	global xmin
	global xmax
	global x_div
	n=data_x.shape[0]
	X_new=np.empty((0,1))
	Y_new=np.empty((0,1))
	X_err_new=np.empty((0,1))
	Y_err_new=np.empty((0,1))
	for ii in range(0,n):
		if data_x[ii]>=x_min and data_x[ii]<=x_max:
			X_new=np.append(X_new,data_x[ii])
			Y_new=np.append(Y_new,data_y[ii])
			X_err_new=np.append(X_err_new,x_err[ii])
			Y_err_new=np.append(Y_err_new,y_err[ii])
	data_x=X_new
	data_y=Y_new
	x_err=X_err_new
	y_err=Y_err_new
	xmin=x_min
	xmax=x_max
	x_div=(xmax-xmin)/100
	return X_new,Y_new,X_err_new,Y_err_new
	
'''
def least_square(a):
	para=[a]
	return sum((data_y-fitfunc(data_x,*para))**2/y_err**2)
'''
