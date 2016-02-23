redirector="root://xrootd-cms.infn.it//"
path_data="store/user/gfasanel/crab_jobs/SingleElectron_0T/CRAB3_TP/160219_153744/0000/TnPTree_data_"
path_data_runC="store/user/gfasanel/crab_jobs/SingleElectron_0T/CRAB3_TP/160219_161759/0000/TnPTree_data_"
path_MC="store/user/gfasanel/crab_jobs_MC/DYToEE_NNPDF30_13TeV-powheg-pythia8/CRAB3_TP/160219_154009/0000/TnPTree_mc_"

################ MC #####################
if [[ $1 = "MC" ]]; then
    echo "[INFO] you are writing hadd_MC.sh"
    printf "hadd -f tp_ntuples/DYToEE_NNPDF30_powheg_76_v2.root " > hadd_MC.sh
    for i in `seq 1 16`; do
	printf ${redirector}${path_MC}${i}.root" " >> hadd_MC.sh
    done
fi
    

################ Data #####################
if [[ $1 = "data" ]]; then
    echo "[INFO] you are writing hadd_data.sh"
    printf "hadd -f tp_ntuples/SingleEle_0T_RunD_76.root " > hadd_data.sh
    for i in `seq 1 55`; do
	printf ${redirector}${path_data}${i}.root" ">> hadd_data.sh
    done
    
    printf "\n" >> hadd_data.sh
    printf "hadd -f tp_ntuples/SingleEle_0T_RunC_76.root " >> hadd_data.sh
    for i in `seq 1 76`; do
	printf ${redirector}${path_data_runC}${i}.root" " >> hadd_data.sh
    done
fi