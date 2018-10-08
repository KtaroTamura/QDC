import myfunc as mf
import ROOT,sys,re
import numpy as np

##Set Up##
bin_min=-100
bin_max=4200.
rebin=int((bin_max-bin_min)/10)

##Myfunc setuop##
mf.depth_Al=0.0
mf.depth_CH=0.1
mf.depth_Pb=0.0
mf.sigma=0.1

##Fitting seup##
ped=52
fit_min=1700.
fit_max=2200.
#h1file="../Canadawork/databox_summer/sdata2018_0137.out"
h1file="../Canadawork/databox_summer/sdata2018_0155.out"

a=7.66474e-04
zero=52.

class Fitting:
	def __call__(self, ch, par):
		C=par[0]
		mf.depth_Al=par[1]
		mf.depth_CH=par[2]
		mf.depth_Pb=par[3]
		T0=a*(ch[0]-zero)
		P=0
		if T0>0 and T0<mf.E_max:
			T=mf.E_correction(T0)
			if T>0 and T<mf.E_max:
				#P=C*mf.G_correction(T)/23700.986076290093
				P=C*mf.Fermi(T)*mf.calc(T)/23700.986076290093
			else:
				P=0	
		return P

if __name__=="__main__":
	##declation##
	ROOT.gStyle.SetOptLogy()
	h1=ROOT.TH1D("h1","data"+h1file.lstrip("./databox_summer/sdata"),rebin,bin_min,bin_max)
	
	##File Read & Fill histgram##
	data=open(h1file,"r")
	for line in data:
		count=int(line)
		h1.Fill(count)
	data.close()
	
	##Fitting##
	f1=ROOT.TF1("f1",Fitting(),fit_min,fit_max,4)
	f1.SetParNames("N_{0}","Al","CH","Pb")
	f1.SetParLimits(3,0.005,0.015)
	f1.SetParameters(2.35e+06,0.03,0.1,0.01)
	f1.FixParameter(1,0.01)
	f1.FixParameter(3,0.01)
#	f1.FixParameter(0,2.3468e+06)
	h1.Fit("f1","","",fit_min,fit_max)
	C=f1.GetParameter(0)
	mf.depth_Al=f1.GetParameter(1)
	mf.depth_CH=f1.GetParameter(2)
	mf.depth_Pb=f1.GetParameter(3)

	##Draw Setup##
	h1.GetXaxis().SetTitle("QDC ch [ch]")
	h1.GetYaxis().SetTitle("Count")
	h1.SetLineColor(4)
	f1.SetLineColor(4)
	h1.Draw()
	
	##Draw TGraph##
	ROOT.gStyle.SetOptFit();
	g1=ROOT.TGraph()
	for ch in range(0,4000,10):	
		t0=a*(ch-zero)
		if t0>2.28:
			break
		if t0>0:
			t=mf.E_correction(t0)
			PY=0
			if t>0 and t<2.28:
				PY=C*mf.G_correction(t)/23700.986076290093		
				#PY=C*mf.Fermi(t)*mf.calc(t)/23700.986076290093	
			y=PY
			g1.SetPoint(ch,ch,y)
#			print("{},{}".format(ch,t))
			if y>0 and y<0.5:
				print("EP={}".format(ch))
				break
	g1.SetMarkerStyle(7)
	g1.Draw("same,P")
'''
	##Save calibration parameters##
	h1file=h1file.lstrip("./data_summer/sdata2018")
	calib_num=int(re.sub(r'\D','',h1file))
	output=[a,C,zero,calib_num]
	np.savetxt("setup_calib.csv",output,delimiter=',')
'''	
def stop(self):
	sys.stderr.write('[Read]\tstop.\tPress "q"to quit >')
	ans=raw_input ('>')
	if ans in ['q','Q']:
		h1.IsA().Destructor(h1)
		fit.IsA().Destructor(fit)
		g1.IsA().Destructor(g1)
		sys.exit(-1)
	elif ans in ['.','q','Q']:
		return -1
