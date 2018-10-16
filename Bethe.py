import myfunc as mf
import numpy as np
import ROOT,sys,re

##Myfunc setuop##
mf.depth_Al=0.02
mf.depth_CH=0.04001
mf.depth_Pb=0.01

if __name__=='__main__':
	T0=np.array([])
	Bethe_Al=np.array([])
	Bethe_CH=np.array([])
	Bethe_Pb=np.array([])
	for e in range(1,1000,10):
		T=0.01*e
		T0=np.append(T0,T)
		Al=mf.bethe(T,'Al')
		CH=mf.bethe(T,'CH')
		Pb=mf.bethe(T,'Pb')
		Bethe_Al=np.append(Bethe_Al,Al)
		Bethe_CH=np.append(Bethe_CH,CH)
		Bethe_Pb=np.append(Bethe_Pb,Pb)
	Bethe_Al=Bethe_Al.flatten()	
	Bethe_CH=Bethe_CH.flatten()	
	Bethe_Pb=Bethe_Pb.flatten()
	n=T0.shape[0]
	ROOT.gStyle.SetOptLogy()
	g1=ROOT.TGraph(n,T0,Bethe_Al)
	g2=ROOT.TGraph(n,T0,Bethe_CH)
	g3=ROOT.TGraph(n,T0,Bethe_Pb)
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
	g3.GetYaxis().SetTitle("Probablity")
	legend=ROOT.TLegend(0.6,0.9,0.89,0.75)
	legend.AddEntry(g1,"Al","l")
	legend.AddEntry(g2,"CH","l")
	legend.AddEntry(g3,"Pb","l")
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
