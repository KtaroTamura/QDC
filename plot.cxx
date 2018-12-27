TString safename(TString name){
	TObject *old=gROOT->FindObject(name);
	if(old) delete old;
	return name;
}

int plot(int run_num){
	//Declaration//
	int x,j=0;
	int rebin=400,bin_min=0,bin_max=4000;
	
	//Naming File&Graph//
	FILE *fp;
	char inputfile[50]={0},graphtitle[50]={0};
	sprintf(inputfile,"../databox/data2018_%04d.out",run_num);
	sprintf(graphtitle,"data2018_%04d.out",run_num);
	
	gStyle->SetOptStat();	
	gStyle->SetOptLogy();
	TH1D *h1=new TH1D(safename("h1"),graphtitle,rebin,bin_min,bin_max);
	

	//File open//
	if((fp=fopen(inputfile,"r"))==NULL){
	printf("file open error!!");
	}

	//Data reading//
	while((fscanf(fp,"%d",&x))!=EOF){
		h1->Fill(x);
		j++;
	}	
	
	//Histgram Draw//
	h1->SetXTitle("QDC channel");
	h1->SetYTitle("Count");
	//h1->Draw("E");
	h1->Draw();
	fclose(fp);
	return 0;
}
