import myfunc as mf
import numpy as np
import ROOT,sys,re

##Myfunc setuop##
mf.depth_Al=0.02
mf.depth_CH=0.04001
mf.depth_Pb=0.01
mf.sigma=0.1

if __name__=='__main__':
	T0=np.array([])
	T1=np.array([])
	Tout=np.array([])
	Pori=np.array([])
	Pout=np.empty([])
	Pin=np.empty([])
	flag=0
	for e in range(1,230):
		T=0.01*e
		T2=mf.int_bethe(T)
		T0=np.append(T0,T)
		T1=np.append(T1,T2)
		P1=mf.Fermi(T)*mf.calc(T)
		Pori=np.append(Pori,P1)
		if T2>0:
			if flag==0:
				print('T={}, T2={}'.format(T,T2))
				flag+=1
			Pin=np.append(Pin,P1)
		else:
			Pin=np.append(Pin,0)	
	mf.depth_Al=0.02
	mf.depth_CH=0.04001+0.00473439
	mf.depth_Pb=0.01
	mf.sigma=0.1
	for e in range(1,230):
		T=0.01*e
		T2=mf.int_bethe(T)
		Tout=np.append(Tout,T2)
		P1=mf.Fermi(T)*mf.calc(T)
		if T2>0:
			Pout=np.append(Pout,P1)
		else:
			Pout=np.append(Pout,0)
	Pori=Pori/Pori.sum()
	Pin=Pin/Pin.sum()
	Pout=Pout/Pout.sum()
	T0=T0.flatten()
	T1=T1.flatten()
	Tout=Tout.flatten()
	Pori=Pori.flatten()
	Pin=Pin.flatten()
	Pout=Pout.flatten()
	n=T0.shape[0]

	ROOT.gStyle.SetOptLogy()
	g1=ROOT.TGraph(n,T0,Pori)
	g2=ROOT.TGraph(n,Tout,Pout)
	g3=ROOT.TGraph(n,T1,Pin)
	g1.SetLineColor(2)	
	g2.SetLineColor(4)	
	g3.SetLineColor(6)	
	g1.SetMarkerColor(2)	
	g2.SetMarkerColor(4)
	g3.SetMarkerColor(6)
	#g1.GetYaxis().SetRangeUser(0,0.01)
	g1.SetLineWidth(3)
	g2.SetLineWidth(3)
	g3.SetLineWidth(3)
	g3.SetTitle("Simulation")
	g3.GetXaxis().SetTitle("Energy [MeV]")
	g3.GetXaxis().SetLimits(0.,2.5)
	g3.GetYaxis().SetTitle("Probablity")
	legend=ROOT.TLegend(0.6,0.9,0.89,0.75)
	legend.AddEntry(g1,"original","l")
	legend.AddEntry(g3,"Inside","l")
	legend.AddEntry(g2,"Outside","l")
	g3.Draw()
	g1.Draw("same")
	g2.Draw("same")
	legend.Draw()

def stop(self):
    sys.stderr.write('[Read]\tstop.\tPress "q"to quit>')
    ans=raw_input ('>')
    if ans in ['q','Q']:
        g1.IsA().Destructor(g1)
        g2.IsA().Destructor(g2)
        g3.IsA().Destructor(g3)
        legned.IsA().Destructor(legend)
        sys.exit(-1)
    elif ans in ['.','q','Q']:
        return -1	
