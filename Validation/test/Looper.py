from ROOT import *
pu_weights_file=TFile("pu_weights_0T.root")
pu_weights=pu_weights_file.Get("pu_weights")
file_MC=TFile('tp_ntuples/DYToEE_NNPDF30_powheg_76_v2.root')
tree_MC=file_MC.Get("PhotonToRECO/fitter_tree")
fileNew=TFile("tp_ntuples/added.root")
treeNew =TTree("puweight_added","puweight_added");

nentriesOrigs=tree_MC.GetEntries()

#original tree leaves
#Int_t           truePU   = 0;

#List of branches - original tree
#TBranch        *b_run; 

# Set branch addresses and branch pointers 
#tree_MC.SetBranchAddress("truePU", &run, &b_run);
tree_MC.SetBranchAddress("truePU", &run, &b_run);


  // New variables
  float tag_pt, tag_absEta;


    // New branches
    theTreeNew->Branch("run", &run, "run/I");


  for(int i=0; i<nentriesOrig; i++) {
    
    if (i%10000 == 0) std::cout << ">>> Event # " << i << " / " << nentriesOrig << " entries" << std::endl; 
    treeOrig->GetEntry(i)


      // now making flat tree
      massRaw = (float)(invMassRaw->at(ii));


      treeNew->Fill();
    }
  }
