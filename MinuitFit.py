import numpy as np
import iminuit as im
import matplotlib.pyplot as plt

##index##
'''
Setup(x,y,xerr,yerr,func,ax)

chisquare(*par,Draw_option)
	least_square1~4(*par)
	|	fitfunc(*par)
	|	project_err(*par)
	|
	Draw_graph(*result_par)

SetLimit(par_limit(min,max))
SetRange(x_limit(xmin,xmax))
'''

sigma=0.1
graph_counter=0

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
	global opt_order
	opt_order=""
	data_x=main_x
	data_y=main_y
	x_err=main_xerr
	y_err=main_yerr
	fitfunc=main_func
	ax=main_ax
	xmin=np.amin(data_x)
	xmax=np.amax(data_x)
	x_div=(xmax-xmin)/100
	if type(x_err)==int or type(x_err)==float:
		x_err=np.full(data_x.shape[0],x_err)
	if type(y_err)==int or type(y_err)==float:
		y_err=np.full(data_x.shape[0],y_err)
	return 0

	
def chisquare(*par,Dopt=True):
	output=[]
	graph_par=[] 
	res_text=''
	par_num=len(par)
	order="global m;m=im.Minuit(least_square{}".format(par_num)
	par_name=["a","b","c","d"]
	for jj in range(0,par_num):
		order=order+",{}=par[{}],error_{}=0.1".format(par_name[jj],jj,par_name[jj])
	order=order+opt_order+",errordef=1)"
	exec(order)
	fmin,param=m.migrad()
	chi=fmin.fval/(len(data_y)-2)
	for ii in range(0,par_num):
		output.extend([param[ii].value,param[ii].error])
		graph_par.extend([param[ii].value])
		onestr='p{}= {} +- {}'.format(ii,param[ii].value,param[ii].error)+'\n'
		res_text=res_text+onestr
	output.append(chi)
	res_text=res_text+'chi2/ndf={}'.format(chi)
	if Dopt==True:
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
	global graph_counter
	gx=np.arange(xmin,xmax,x_div)
	fit_line=fitfunc(gx,*para)
	ax.plot(gx,fit_line,color='r')
	if graph_counter==0:
		textstr=r'$\chi^2=%.2f$' % (k, )
		par_num=len(para)
		for i in range(0,par_num):
			one='\n'+r'$p{}={:.4E}$'.format(i,para[i])
			textstr=textstr+one
		props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
		plt.text(0.7,0.98,textstr,transform=ax.transAxes,fontsize=10,verticalalignment='top', bbox=props)
		graph_counter=1
	return 0

#
def project_err(*para):
	dh=0.001
	dfdx=(fitfunc(data_x+dh,*para)-fitfunc(data_x,*para))/dh
	vir_err=dfdx*x_err
	return vir_err

def fitfunc():
	return 0

def SetLimit(*ppap,lim_a=False,lim_b=False,lim_c=False,lim_d=False):
	global opt_order
	opt_order=""
	lim_par=[lim_a,lim_b,lim_c,lim_d]
	limitter=['limit_a','limit_b','limit_c','limit_d']
	par_name=["a","b","c","d"]
	for kk in range(0,4):
		if lim_par[kk]!=False:
			opt_order=opt_order+",{}={}".format(limitter[kk],lim_par[kk])
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
			print("{}".format(data_x[ii]))
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
	
