import numpy as np 
import ROOT,sys,csv,math
import myfunc as mf 


##Set Up##
bin_min=-420
bin_max=4200.
rebin=int((bin_max-bin_min)/10)
h1file="../databox/data2018_0080.out"
h2file="../databox/data2018_0081.out"

##Depth setup##
depthA_Al=0.01
depthA_CH=0.01
depthB_Al=0.01
depthB_CH=0.01


##integral_bethe##
def int_betheA(T):
	mf.depth_Al=depthA_Al
	mf.depth_CH=depthA_CH
	T0=T
	if T0>0.5:
		for l in range(0,9):
			if T0>0:
				eloss=(mf.bethe(T0,'Al')+mf.bethe(T0,'CH'))*0.1
				T0=T0-eloss
			if T0<0:
				T0=T0-eloss
				break
	elif T0<0.5:
		T0=T0-(mf.bethe(T0,'Al')+mf.bethe(T0,'CH'))
	return T0

def int_betheB(T):
	mf.depth_Al=depthB_Al
	mf.depth_CH=depthB_CH
	T0=T
	if T0>0.5:
		for l in range(0,9):
			if T0>0:
				eloss=(mf.bethe(T0,'Al')+mf.bethe(T0,'CH'))*0.1
				T0=T0-eloss
			if T0<0:
				T0=T0-eloss
				break
	elif T0<0.5:
		T0=T0-(mf.bethe(T0,'Al')+mf.bethe(T0,'CH'))
	return T0

##Energy_correction##
def E_correction(T,x):
	pre_delta=0.5
	E_emit=0
	for L in range(1,100):
		loss=0.01*L
		t=T+loss
		if T+loss>0:
			if x==1:
				M=t-int_betheA(t)
			elif x==2:
				M=t-int_betheB(t)
			delta=abs(M-loss)
			if delta<pre_delta:
				pre_delta=delta
				E_emit=t
			elif delta<0.001:
				pre_delta=delta
				E_emit=t
				break
	return E_emit

if __name__=="__main__":
###Declaration###	
	ROOT.gStyle.SetOptStat(0)
	cv=ROOT.TCanvas("cv","cv",0,0,1200,800)
	h1=ROOT.TH1D("h1","data"+h1file.lstrip("../databox"),rebin,bin_min,bin_max)
	h2=ROOT.TH1D("h2","data"+h2file.lstrip("../databox"),rebin,bin_min,bin_max)

###data read###
	data=open(h1file,"r")
	for line in data:
		count=int(line)
		h1.Fill(count)
	data.close()
	data2=open(h2file,"r")
	for line2 in data2:
		count2=int(line2)
		h2.Fill(count2)
	data2.close()

###Parameter read###
	calib_data=np.loadtxt("setup_calib.csv",delimiter=",",skiprows=0)
	a=calib_data[0]
	C=calib_data[1]
	zero=calib_data[2]
	calib_num='%04d' % calib_data[3]
	
###Set Graph data###
	g1=ROOT.TGraphErrors()
	g2=ROOT.TGraphErrors()
	g11=ROOT.TGraphErrors()
	g22=ROOT.TGraphErrors()
	for bin_num in range(1,410):
		ch=(bin_num-1)*10+5
		T0=a*((bin_num-1+bin_min/10)*10+5-zero)
		T=E_correction(T0,1)
		count_bin=h1.GetBinContent(bin_num)
		count_error=math.sqrt(count_bin)
		g1.SetPoint(bin_num-1,T0,count_bin)
		g1.SetPointError(bin_num-1,0,count_error)
		g11.SetPoint(bin_num-1,T,count_bin)
		g11.SetPointError(bin_num-1,0,count_error)
		if T>2.4:
			break
	
	for bin_num2 in range(1,410):
		ch2=(bin_num2-1)*10+5
		T02=a*((bin_num2-1+bin_min/10)*10+5-zero)
		T2=E_correction(T02,2)
		count_bin2=h2.GetBinContent(bin_num2)
		count_error2=math.sqrt(count_bin2)
		g2.SetPoint(bin_num2-1,T02,count_bin2)
		g2.SetPointError(bin_num2-1,0,count_error2)
		g22.SetPoint(bin_num2-1,T2,count_bin2)
		g22.SetPointError(bin_num2-1,0,count_error2)
		if T2>2.4:
			break

###Canvas1###	
	cv.Divide(1,3)
	cv.cd(1)
	h2.GetXaxis().SetTitle("QDC ch [ch]")
	h2.GetYaxis().SetTitle("Count")
	h1.SetLineColor(2)
	h2.SetLineColor(4)
	leg=ROOT.TLegend(0.7,0.65,0.85,0.85)
	leg.AddEntry(h1,h1file.lstrip("../databox/"),"l")
	leg.AddEntry(h2,h2file.lstrip("../databox/"),"l")
	h2.Draw()
	h1.Draw("same")
	leg.Draw()
###Canvas2###
	cv.cd(2)
	g2.SetMarkerStyle(7)
	g2.SetLineColor(4)
	g2.SetMarkerColor(4)
	g2.SetTitle("Detected Spectrum")
	g2.GetXaxis().SetTitle("Detcted Energy [MeV]")
	g2.GetYaxis().SetTitle("Count")
	g1.SetMarkerStyle(7)
	g1.SetLineColor(2)
	g1.SetMarkerColor(2)
	g1.SetTitle("Detected Spectrum")
	g1.GetXaxis().SetTitle("Detected Energy [MeV]")
	g1.GetYaxis().SetTitle("Count")
	g1.GetYaxis().SetRangeUser(0,3500)
	g1.Draw()
	g2.Draw("same")
###Canvas3###
	cv.cd(3)
	c3title="Calibration Spectrum (by data2018_"+calib_num+".out)"
	g22.SetMarkerStyle(7)
	g22.SetLineColor(4)
	g22.SetMarkerColor(4)
	g22.SetTitle(c3title)
	g22.GetXaxis().SetTitle("Energy at emission [MeV]")
	g22.GetYaxis().SetTitle("Count")
	g11.SetMarkerStyle(7)
	g11.SetLineColor(2)
	g11.SetMarkerColor(2)
	g22.Draw()
	g11.Draw("same")


def stop(self):
	sys.stderr.write('[Read]\tstop.\tPress "q"to quit >')
	ans=raw_input ('>')
	if ans in ['q','Q']:
		cv.IsA().Destructor(cv)
		h1.IsA().Destructor(h1)
		h2.IsA().Destructor(h2)
		leg.IsA().Destructor(leg)
		g1.IsA().Destructor(g1)
		g2.IsA().Destructor(g2)
		g11.IsA().Destructor(g11)
		g22.IsA().Destructor(g22)
		sys.exit(-1)
	elif ans in ['.','q','Q']:
		return -1
