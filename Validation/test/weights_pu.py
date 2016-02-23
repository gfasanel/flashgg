from ROOT import *
_file0=TFile("puTarget2015.root")
pu_target =_file0.Get("pu")
pu_target.Scale(1./pu_target.Integral())
_file1=TFile("tp_ntuples/DYToEE_NNPDF30_powheg_76_v2.root")
mc = _file1.Get("PhotonToRECO/fitter_tree")
mc.Draw("truePU>>pu_mc(52,0,52)")
pu_mc.Scale(1./pu_mc.Integral())
pu_weights = pu_target.Clone("pu_weights");
pu_weights.Divide(pu_mc);
pu_weights.SaveAs("pu_weights_0T.root");


