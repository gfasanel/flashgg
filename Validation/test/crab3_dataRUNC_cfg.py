from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'flashgg_TP_data_RUNC'
config.General.workArea = 'crab_data_TP_76'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'makeTreePhotons_0T.py'
config.Data.inputDataset = '/SingleElectron_0T/gfasanel-0T_76-1_1_0-v0-Run2015C_25ns-27Jan2016-v2-7e516a39f82db69021bdfacbf5667a6f/USER'
#config.Data.inputDBS = 'global'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 100
config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions15/13TeV/Cert_246908-260627_13TeV_PromptReco_Collisions15_ZeroTesla_25ns_JSON.txt'
#config.Data.runRange = '193093-193999' # '193093-194075'
config.Data.outLFNDirBase = '/store/user/gfasanel/crab_jobs/' 
config.Data.publication = False
config.Data.outputDatasetTag = 'CRAB3_TP'
#config.Site.storageSite = 'T2_CH_CERN'
config.Site.storageSite = 'T2_IT_Rome'
config.JobType.pyCfgParams=['isMC=False']
