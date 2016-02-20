from ROOT import *
gROOT.SetBatch(kTRUE)
gSystem.Load("~/rootlogon_C.so")
ROOT.rootlogon()

import os

variables=['probe_Pho_sipip',
           'probe_Pho_sieie',
           'probe_Pho_nTrkSolidCone03',
           'probe_Pho_egPhotonIso',
           'probe_Pho_abseta',       
           'probe_Pho_e',            
           'probe_Pho_et',           
           'probe_Pho_eta',          
           'probe_Pho_full5x5x_r9',  
           'probe_Pho_hoe',          
           'probe_Pho_missingHits',  
           'tag_Pho_abseta',         
           'tag_Pho_e',              
           'tag_Pho_et',             
           'pair_mass',              
           'mass'           
           ]

#variables=['probe_Pho_sipip'] #just to test one variable
variables=['mass'] #just to test one variable

hist={}
hist['probe_Pho_sipip'          ]=dict(name='#sigma_{i#phi i#phi}'     ,unit=''     ,bins=100,xmin=0.,xmax=0.05) 
hist['probe_Pho_sieie'          ]=dict(name='probe_Pho_sieie'          ,unit=''     ,bins=400,xmin=0.,xmax=0.05) 
hist['probe_Pho_nTrkSolidCone03']=dict(name='probe_Pho_nTrkSolidCone03',unit=''     ,bins=5,xmin=0.,xmax=5) 
hist['probe_Pho_egPhotonIso'    ]=dict(name='probe_Pho_egPhotonIso'    ,unit=''     ,bins=100,xmin=0.,xmax=5) 
hist['probe_Pho_abseta'         ]=dict(name='probe_Pho_abseta'         ,unit=''     ,bins=100,xmin=0.,xmax=5) 
hist['probe_Pho_e'              ]=dict(name='probe_Pho_e'              ,unit='[GeV]',bins=150,xmin=0.,xmax=300) 
hist['probe_Pho_et'             ]=dict(name='probe_Pho_et'             ,unit='[GeV]',bins=100,xmin=0.,xmax=200) 
hist['probe_Pho_eta'            ]=dict(name='probe_Pho_eta'            ,unit=''     ,bins=100,xmin=-3,xmax=3) 
hist['probe_Pho_full5x5x_r9'    ]=dict(name='probe_Pho_full5x5x_r9'    ,unit=''     ,bins=400,xmin=0.,xmax=1) 
hist['probe_Pho_hoe'            ]=dict(name='probe_Pho_hoe'            ,unit=''     ,bins=100,xmin=0.,xmax=0.1) 
hist['probe_Pho_missingHits'    ]=dict(name='probe_Pho_missingHits'    ,unit=''     ,bins=5,xmin=0.,xmax=5) 
hist['tag_Pho_abseta'           ]=dict(name='tag_Pho_abseta'           ,unit=''     ,bins=100,xmin=0.,xmax=3) 
hist['tag_Pho_e'                ]=dict(name='tag_Pho_e'                ,unit='[GeV]',bins=100,xmin=0.,xmax=200) 
hist['tag_Pho_et'               ]=dict(name='tag_Pho_et'               ,unit='[GeV]',bins=100,xmin=0.,xmax=200) 
hist['pair_mass'                ]=dict(name='pair_mass'                ,unit='[GeV]',bins=60,xmin=70.,xmax=110) 
hist['mass'                     ]=dict(name='mass'                     ,unit='[GeV]',bins=60,xmin=70.,xmax=110) 

#( isEB && full5x5_sigmaIetaIeta < 1.05e-2 && sqrt(sipip)< 1.05e-2 && nTrkSolidConeDR03 < 4  && egPhotonIso<3 )
#file_MC=TFile('tp_ntuples/DYToEE_NNPDF30_powheg.root')
file_MC=TFile('tp_ntuples/DYToEE_NNPDF30_powheg_76_v2.root')
tree_MC=file_MC.Get("PhotonToRECO/fitter_tree")

#file_data=TFile('tp_ntuples/SingleEle_0T_RunDv4.root')
file_data=TFile('tp_ntuples/SingleEle_0T_RunD_76.root')
tree_data=file_data.Get('PhotonToRECO/fitter_tree')

#Cuts####################################
mass_cut="(pair_mass>80)&&(pair_mass<100)"
extra_mass_cut="(pair_mass>75)&&(pair_mass<95)"

probe_barrel="(probe_Pho_abseta<1.442)"
tag_barrel="(tag_Pho_abseta<1.442)"
probe_endcap="(probe_Pho_abseta>1.566)&&(probe_Pho_abseta<2.5)"
tag_endcap="(tag_Pho_abseta>1.566)&&(tag_Pho_abseta<2.5)"

eb_eb=probe_barrel+"&&"+tag_barrel
eb_ee="(("+probe_barrel+"&&"+tag_endcap+") || ("+probe_endcap+"&&"+tag_barrel+"))"
#ele_sel="passingEleSel"
ele_sel="(probe_Pho_missingHits>=0)&&(probe_Pho_missingHits<=1)"

############################################
selection_bb=eb_eb+"&&"+mass_cut
selection_be=eb_ee+"&&"+mass_cut
selection_bb_ele=selection_bb+"&&"+ele_sel
selection_be_ele=selection_be+"&&"+ele_sel
############################################
selection_barrel=probe_barrel+"&&"+mass_cut
selection_barrel_ele=selection_barrel+"&&"+ele_sel
selection_endcap=probe_endcap #+"&&"+mass_cut
selection_endcap_ele=selection_endcap+"&&"+ele_sel

#sel_names=['bb','be','bb_ele','be_ele']
sel_names=['barrel','endcap','barrel_ele','endcap_ele']
selection={}
##########################################
selection['bb']=selection_bb
selection['be']=selection_be
selection['bb_ele']=selection_bb_ele
selection['be_ele']=selection_be_ele
##########################################

selection['barrel']=selection_barrel
selection['barrel_ele']=selection_barrel_ele
selection['endcap']=selection_endcap
selection['endcap_ele']=selection_endcap_ele

#print selection['barrel']
#print selection['barrel_ele']
#print selection['endcap']
#print selection['endcap_ele']

y_scales=['lin','log']
y_factor={}
y_factor['lin']=1.2
y_factor['log']=10

for variable in variables:
   print "[INFO] Plotting ",variable
   for sel_name in sel_names:
      print "[INFO] Sel name ",sel_name 
      print "[INFo] Corresponding selection is ",selection[sel_name]
      for y_scale in y_scales:
         canvas=TCanvas()
         scale=y_factor[y_scale]
         pad1 = TPad("pad1", "pad1",0.00,0.25, 1,1.);
         pad2 = TPad("pad2", "pad2",0.00,0.00, 1,0.25);
         
         yscale=0.75/(pad1.GetYlowNDC() -pad2.GetYlowNDC());
         pad1.SetBottomMargin(0.02);
         pad1.Draw();
         pad2.SetGrid();
         pad2.SetTopMargin(0.03);
         pad2.SetBottomMargin(0.4);
         pad2.Draw();

         
         pad1.cd();
         h_MC=TH1F("h_MC","h_MC_"+selection[sel_name]+"_"+variable,hist[variable]['bins'],hist[variable]['xmin'],hist[variable]['xmax'])
         h_data=TH1F("h_data","h_data_"+selection[sel_name]+"_"+variable,hist[variable]['bins'],hist[variable]['xmin'],hist[variable]['xmax'])
         tree_MC.Draw(variable+">>h_MC",selection[sel_name]+"&&"+mass_cut)
         if sel_name in ('endcap','endcap_ele') :
            tree_data.Draw(variable+">>h_data",selection[sel_name]+"&&"+extra_mass_cut) 
         else:
            tree_data.Draw(variable+">>h_data",selection[sel_name]+"&&"+mass_cut) 
         if y_scale!='lin':
            print "[INFO] Setting log scale"
            canvas.cd(1)
            gPad.SetLogy(1)
            h_MC.SetMinimum(0.0001)
         h_MC.Sumw2()
         h_data.Sumw2()
         h_MC.GetYaxis().SetTitle("Normalized events")
         h_MC.SetLineColor(kRed)
         h_MC.SetFillColor(kRed)
         h_MC.SetFillStyle(3001)
         h_data.SetLineColor(kBlack)
         h_MC.GetXaxis().SetLabelSize(0)
         h_MC.Scale(1./h_MC.Integral())
         h_data.Scale(1./h_data.Integral())
         my_max=max(h_MC.GetMaximum(),h_data.GetMaximum())
         h_MC.SetMaximum(my_max*scale)
         h_MC.Draw("hist")
         h_data.SetMarkerSize(0.8)
         h_data.Draw("psame")
         legend=TLegend(0.6,0.6,0.8,0.8)
         legend.SetBorderSize(0)
         legend.SetFillColor(0);
         legend.SetFillStyle(1001);
         legend.SetTextFont(22); 
         legend.SetTextSize(0.03);
         legend.AddEntry(h_MC,"MC DY powheg 0T","f");
         legend.AddEntry(h_data,"Single Electron 0T","l");
         legend.Draw()
         if sel_name in ('barrel','barrel_ele'):
            label_region =TLatex(0.2,0.8,"EB")
            label_region.SetNDC()
            label_region.Draw()
         else:
            label_region =TLatex(0.2,0.8,"EE")
            label_region.SetNDC()
            label_region.Draw()

         
         pad2.cd();
         sRatio = h_data.Clone("sRatio");
         sRatio.Divide(h_MC);
         sRatio.Draw();
         ratioGraph = TGraphErrors(sRatio);
         ratioGraph.SetMarkerColor(kBlack);
         ratioGraph.SetMarkerStyle(20);
         ratioGraph.SetMarkerSize(0.7);
         ratioGraph.Draw("AP");
         ratioGraph.GetXaxis().SetRangeUser(h_MC.GetXaxis().GetXmin(),h_MC.GetXaxis().GetXmax());
      #ratioGraph.GetXaxis().SetTitle(mc.GetXaxis().GetTitle());
         ratioGraph.GetYaxis().SetTitle("Data/MC");
         ratioGraph.GetYaxis().SetTitleSize(sRatio.GetYaxis().GetTitleSize()*yscale);
         ratioGraph.GetYaxis().SetTitleOffset(0.3);
         ratioGraph.GetYaxis().SetLabelSize(sRatio.GetYaxis().GetLabelSize()*yscale);
         ratioGraph.GetYaxis().SetLabelOffset(sRatio.GetYaxis().GetLabelOffset()*yscale);
         ratioGraph.GetXaxis().SetTitleSize(sRatio.GetYaxis().GetTitleSize() *yscale   );
         ratioGraph.GetXaxis().SetTitleOffset(0.92);
         ratioGraph.GetXaxis().SetLabelSize(sRatio.GetYaxis().GetLabelSize() *yscale   );
         ratioGraph.GetXaxis().SetLabelOffset(sRatio.GetYaxis().GetLabelOffset());
         ratioGraph.GetXaxis().SetTitle(hist[variable]['name']+hist[variable]['unit'])
      #ratioGraph.GetYaxis().SetRangeUser(1- 2*ratioGraph.GetRMS(2),1+2*ratioGraph.GetRMS(2));
         ratioGraph.GetYaxis().SetRangeUser(0.2,4);
         ratioGraph.GetYaxis().SetNdivisions(5);

         
         canvas.SaveAs("~/scratch1/www/TP/76/data_MC/"+variable+"_"+sel_name+"_"+y_scale+".png")
      
