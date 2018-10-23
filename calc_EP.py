import myfunc as mf
import ROOT,sys,re
import numpy as np

##Set Up##
bin_min=0
bin_max=4200.
rebin=int((bin_max-bin_min)/10)

##Myfunc setuop##

##Fitting seup##
'''
a=7.47429e-04
C=7.95340e+05
zero=52
mf.depth_Al=5.35794e-03
mf.depth_CH=0.
mf.depth_Pb=0.
mf.sigma=1.42911e-02

'''
a=7.47429e-04
C=9.342e+05
zero=52
mf.depth_Al=0.01
mf.depth_CH=0.03963
mf.depth_Pb=0.008
mf.sigma=1.42911e-02


#h1file="../Canadawork/databox_summer/sdata2018_0137.out"
h1file="../Canadawork/databox_summer/sdata2018_0155.out"

if __name__=="__main__":
	##declation##
	ROOT.gStyle.SetOptLogy()
	h1=ROOT.TH1D("h1","data"+h1file.lstrip("..Canadawork/databox_summer/sdata"),rebin,bin_min,bin_max)

##File Read & Fill histgram##
	data=open(h1file,"r")
	for line in data:
		count=int(line)
		h1.Fill(count)
	data.close()


	##Draw Setup##
	h1.GetXaxis().SetTitle("QDC ch [ch]")
	h1.GetYaxis().SetTitle("Count")
	h1.SetLineColor(4)
	h1.Draw()

	##Draw TGraph##
	ROOT.gStyle.SetOptFit();
	g1=ROOT.TGraph()
	for ch in range(0,3200):	
		t0=a*(ch-zero)
		if t0>2.28:
			break
		if t0>0:
			t=mf.E_correction(t0)
			PY=0
			if t>0 and t<2.28:
				PY=C*mf.G_correction(t)/23700.986076290093
			y=PY
			g1.SetPoint(ch,ch,y)
		#	print("{},{}".format(ch,t))
			if y>0 and y<0.5:
				print("EP={}".format(ch))
				break
	g1.SetMarkerStyle(7)
	g1.SetLineWidth(2)
	g1.SetLineColor(2)
	g1.Draw("same")

def stop(self):
	sys.stderr.write('[Read]\tstop.\tPress "q"to quit >')
	ans=raw_input ('>')
	if ans in ['q','Q']:
		h1.IsA().Destructor(h1)
		fit.IsA().Destructor(fit)
#		g1.IsA().Destructor(g1)
		sys.exit(-1)
	elif ans in ['.','q','Q']:
		return -1
