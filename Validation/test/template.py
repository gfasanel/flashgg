from ROOT import *
gROOT.SetBatch(kTRUE)

file_MC=TFile("~/scratch1/Test_7_6/CMSSW_7_6_3/src/flashgg/Validation/test/tp_ntuples/DYToEE_NNPDF30_powheg_76_v2_optimizedID.root")
tree_MC=file_MC.Get("PhotonToRECO/fitter_tree")
#####################################
pu_weights_file=TFile("pu_weights_0T.root")
pu_weights=pu_weights_file.Get("pu_weights")
pu_reweight_string="("
for i in range(1,pu_weights.GetSize()-3):
   #bin1 means pu 0
   pu_reweight_string+="(truePU=="+str(i-1)+")*"+str(pu_weights.GetBinContent(i))+" + "
pu_reweight_string+="(truePU=="+str(pu_weights.GetSize()-3)+")*"+str(pu_weights.GetBinContent(pu_weights.GetSize()-2))+" ) "
#####################################
etaLow=[0,1.5]
etaHigh=[1.5,2.5]
ptLowBarrel =[20,30,40,50,60,80,110,150,200,270]
ptHighBarrel=[30,40,50,60,80,110,150,200,270,500]
ptLowEndcap =[20,30,40,50,60,80,110,150,200]
ptHighEndcap=[30,40,50,60,80,110,150,200,500]
types=['Pass','Fail','All']
####################################################
selection={}
selection['Pass']="passingSel*mcTrue"
selection['Fail']="(!passingSel)*mcTrue"
selection['All'] ="mcTrue"

output_file=TFile("MCtemplates.root","RECREATE")
output_file.cd()
histos={}
for i in range(len(etaLow)):
   if(etaHigh[i]==1.5):
      for j in range(len(ptLowBarrel)):         
         for type in types:
            range_sel="(probe_Pho_abseta>"+str(etaLow[i])+")*(probe_Pho_abseta<"+str(etaHigh[i])+")*(probe_Pho_et>"+str(ptLowBarrel[j])+")*(probe_Pho_et<"+str(ptHighBarrel[j])+")"
            sel=selection[type]+"*"+range_sel
            temp=TH1F("temp","temp",80,70,110)
            tree_MC.Draw("mass>>temp",sel)
            histos['hMass_'+str(etaLow[i])+"_"+str(etaHigh[i])+"_"+str(ptLowBarrel[j])+"_"+str(ptHighBarrel[j])+"_"+type]=temp.Clone('hMass_'+str(etaLow[i])+"_"+str(etaHigh[i])+"_"+str(ptLowBarrel[j])+"_"+str(ptHighBarrel[j])+"_"+type)
            histos['hMass_'+str(etaLow[i])+"_"+str(etaHigh[i])+"_"+str(ptLowBarrel[j])+"_"+str(ptHighBarrel[j])+"_"+type].Write()
            del temp
   if(etaHigh[i]==2.5):
      for j in range(len(ptLowEndcap)):         
         for type in types:
            range_sel="(probe_Pho_abseta>"+str(etaLow[i])+")*(probe_Pho_abseta<"+str(etaHigh[i])+")*(probe_Pho_et>"+str(ptLowEndcap[j])+")*(probe_Pho_et<"+str(ptHighEndcap[j])+")"
            sel=selection[type]+"*"+range_sel
            temp=TH1F("temp","temp",80,70,110)
            tree_MC.Draw("mass>>temp",sel)
            histos['hMass_'+str(etaLow[i])+"_"+str(etaHigh[i])+"_"+str(ptLowEndcap[j])+"_"+str(ptHighEndcap[j])+"_"+type]=temp.Clone('hMass_'+str(etaLow[i])+"_"+str(etaHigh[i])+"_"+str(ptLowEndcap[j])+"_"+str(ptHighEndcap[j])+"_"+type)
            histos['hMass_'+str(etaLow[i])+"_"+str(etaHigh[i])+"_"+str(ptLowEndcap[j])+"_"+str(ptHighEndcap[j])+"_"+type].Write()
            del temp
     
output_file.Close()

#print pu_reweight_string
##presel="(probe_Pho_full5x5x_r9>0.8)&&(probe_Pho_hoe<0.1)&&(probe_Pho_egPhotonIso<5)&&(probe_Pho_nTrkSolidCone03<5)"

