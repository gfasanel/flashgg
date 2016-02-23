from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'flashgg_TP'
config.General.workArea = 'crab_MC_TP_76'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'Analysis'
#config.JobType.psetName = 'flashgg/MicroAOD/test/microAODstd.py'
#config.JobType.psetName = 'flashgg/Validation/test/makeTreePhotons_0T.py'
config.JobType.psetName = 'makeTreePhotons_0T.py'

#config.Data.inputDataset = '/DoublePhotonHighPt/Tier0_Test_SUPERBUNNIES_vocms047-PromptReco-v66/MINIAOD'
#config.Data.inputDataset = '/DoubleEG_0T/spigazzi-diphotons0T_v1-1_2_0-64-gbd0a265-v0-Run2015D-PromptReco-v4-6d5ef1f49a55061d65937752a97ec87f/USER'
#config.Data.inputDataset = '/DYToEE_NNPDF30_13TeV-powheg-pythia8/spigazzi-diphotons0T_v1-1_2_0-64-gbd0a265-v0-RunIISpring15DR74-0TPU25nsData2015v1_magnetOffBS0T_74X_mcRun2_0T_v0-v2-cafa0a22f06c4afe922304225f67d4ca/USER'
config.Data.inputDataset = '/DYToEE_NNPDF30_13TeV-powheg-pythia8/gfasanel-0T_76-1_1_0-v0-RunIIFall15MiniAODv2-magnetOffBS0T_PU25nsData2015v1_0T_76X_mcRun2_0T_v1-v1-10cefffd95180452da85ecf42ecfcc48/USER'
#config.Data.inputDBS = 'global'
config.Data.inputDBS = 'phys03'
#config.Data.splitting = 'LumiBased'
#config.Data.unitsPerJob = 20
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 5

config.Data.outLFNDirBase = '/store/user/gfasanel/crab_jobs_MC/' 
config.Data.publication = False
config.Data.outputDatasetTag = 'CRAB3_TP'
#config.Site.storageSite = 'T2_CH_CERN'
config.Site.storageSite = 'T2_IT_Rome'
###config.JobType.pyCfgParams=['isGrid=True','isData=False','is25ns=True','is50ns=False
