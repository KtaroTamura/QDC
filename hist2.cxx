TString safename(TString name){
	TObject *old=gROOT->FindObject(name);
	if(old) delete old;
	return name;
}

int hist2(int run_num){
	//Declaration//
	int x,j=0;
	int rebin=4000,bin_min=0,bin_max=4000;
	int fmin,fmax;
	double N,dN;	

	fmin=3500;
	fmax=4000;
	
	//Naming File&Graph//
	FILE *fp,*fout;
	char inputfile[50]={0},graphtitle[50]={0};
	sprintf(inputfile,"../Canadawork/databox_summer/sdata2018_%04d.out",run_num);
	sprintf(graphtitle,"data2018_%04d.out",run_num);
	
	gStyle->SetOptStat();	
	gStyle->SetOptLogy();
	TH1D *h1=new TH1D(safename("h1"),graphtitle,rebin,bin_min,bin_max);
	TF1 *f1=new TF1("f1","gaus(0)",0,4000);

	//File open//
	if((fp=fopen(inputfile,"r"))==NULL){
	printf("file open error!!");
	}

	//Data reading//
	while((fscanf(fp,"%d",&x))!=EOF){
		if((x>=fmin)&&(x<=fmax)){
			h1->Fill(x);
			j++;
		}
	}	
	
	//Histgram Draw//
	h1->SetXTitle("QDC channel");
	h1->SetYTitle("Count");
	f1->SetParLimits(1,fmin,fmax);
	h1->Fit("f1","","",fmin,fmax);
	N=h1->GetMean();
	dN=h1->GetStdDev();
	if((fout=fopen("Linearity.csv","a"))!=NULL){
		//fprintf(fout,"%d,%f,%f\n",run_num,N,dN);
	}
	h1->Draw();	
	fclose(fp);
	fclose(fout);
	return 0;
}
