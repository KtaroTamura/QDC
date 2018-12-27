TString safename(TString name){                                                 
    TObject *old=gROOT->FindObject(name);
    if(old) delete old;
    return name;
}

int kplot(int run_num,int run_num2){	

	//Declaration//
	int x,y;
	int rebin=400,bin_min=0,bin_max=4000;	
	FILE *fpA,*fpB;
	char inputfileA[50]={0},inputfileB[50]={0},gtitle[50]={0},nameA[50]={0},nameB[50]={0};
	int maxA,maxB;

	//Naming file & graph//
	sprintf(inputfileA,"../databox/data2018_%04d.out",run_num);
	sprintf(inputfileB,"../databox/data2018_%04d.out",run_num2);
	sprintf(gtitle,"QDCdata2018_%04d and %04d",run_num,run_num2);
	sprintf(nameA,"%04d",run_num);
	sprintf(nameB,"%04d",run_num2);	
	
	//TCanvas *c1=new TCanvas(safename("c1"),"title",1600,0,800,600);
	TH1D *h1=new TH1D(safename(nameA),gtitle,rebin,bin_min,bin_max);
	TH1D *h2=new TH1D(safename(nameB),gtitle,rebin,bin_min,bin_max);
	
	//File open //
	if((fpA=fopen(inputfileA,"r"))==NULL){
		printf("file open error!!");
	}		
	if((fpB=fopen(inputfileB,"r"))==NULL){
    	printf("file2 open error!!");
	}	

	//File reading//
	while((fscanf(fpA,"%d",&x))!=EOF){
		h1->Fill(x);
	}
	while((fscanf(fpB,"%d",&y))!=EOF){
		h2->Fill(y);
	}

	//Histgram setting//
	maxA=h1->GetMaximum();
	maxB=h2->GetMaximum();
	h1->SetLineColor(kRed);
	h2->SetLineColor(kBlue);
	if(maxA>maxB){
		h1->GetXaxis()->SetTitle("QDC ch [ch]");
		h1->GetYaxis()->SetTitle("count ");
		h1->Draw();
		h2->Draw("sames");
	}else{
		h2->GetXaxis()->SetTitle("QDC ch [ch]");
		h2->GetYaxis()->SetTitle("count ");
		h2->Draw();
		h1->Draw("sames");	
	}
	gPad->Update();

	//infobox setting//
    TPaveStats* st1=(TPaveStats*)h1->FindObject("stats");
    TPaveStats* st2=(TPaveStats*)h2->FindObject("stats");   

    st1->SetX1NDC(0.5);
    st1->SetX2NDC(0.7);
    st1->SetY1NDC(0.7);
    st1->SetY2NDC(0.9);
	st1->SetTextColor(kRed);

    st2->SetX1NDC(0.7);
    st2->SetX2NDC(0.9);
    st2->SetY1NDC(0.7);
    st2->SetY2NDC(0.9);
	st2->SetTextColor(kBlue);
	
	gPad->Modified();
	gPad->Update();

	//file close//
	fclose(fpA);
	fclose(fpB);
	return 0;
}
