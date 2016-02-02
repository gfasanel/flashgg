import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
import sys

process = cms.Process("tnp")

###################################################################
options = dict()
varOptions = VarParsing('analysis')
varOptions.register(
    "isMC",
    True,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Compute MC efficiencies"
    )

varOptions.parseArguments()

options['HLTProcessName']        = "HLT"

photonID_0T = """
(
( isEB && full5x5_sigmaIetaIeta < 1.05e-2 && sqrt(sipip)< 1.05e-2 && nTrkSolidConeDR03 < 4  && egPhotonIso<3 ) 
||
( isEE && full5x5_sigmaIetaIeta < 2.8e-2 && sqrt(sipip)< 2.6e-2 && nTrkSolidConeDR03 < 4  && egPhotonIso<3 )
)
"""

electron_0T="(matchedGsfTrackInnerMissingHits>=0 && matchedGsfTrackInnerMissingHits<2)"


options['PHOTON_COLL']           = "flashggRandomizedPhotons"
options['DIPHOTON_COLL']         = "flashggDiPhotons"
options['PHOTON_CUTS']           = "(abs(superCluster.eta)<2.5) && !(1.4442<=abs(superCluster.eta)<=1.566) && ((superCluster.energy*sin(superCluster.position.theta))>25.0)"
options['PHOTON_SEL_CUTS']           = options['PHOTON_CUTS'] + " && "+ photonID_0T
options['PHOTON_SEL_ELE_CUTS']           = options['PHOTON_SEL_CUTS'] + " && " + electron_0T
options['PHOTON_TAG_CUTS']       = options['PHOTON_CUTS'] + "&& (superCluster.energy*sin(superCluster.position.theta)>30.0)" + " && "+ photonID_0T+ " && " + electron_0T

print "TAG SELECTION: "+options['PHOTON_TAG_CUTS']
print "PROBE SELECTION: "+options['PHOTON_CUTS']

options['MAXEVENTS']             = cms.untracked.int32(-1) 
options['useAOD']                = cms.bool(False)
options['OUTPUTEDMFILENAME']     = 'edmFile.root'
options['DEBUG']                 = cms.bool(True)

from flashgg.Validation.treeMakerOptionsPhotons_0T_cfi import *

if (varOptions.isMC):
    options['INPUT_FILE_NAME']       = ("/store/user/spigazzi/flashgg/diphotons0T_v1/1_2_0-64-gbd0a265/DYToEE_NNPDF30_13TeV-powheg-pythia8/diphotons0T_v1-1_2_0-64-gbd0a265-v0-RunIISpring15DR74-0TPU25nsData2015v1_magnetOffBS0T_74X_mcRun2_0T_v0-v2/160127_134011/0000/myMicroAODOutputFile_250.root")

    options['OUTPUT_FILE_NAME']      = "TnPTree_mc.root"
    options['TnPPATHS']              = cms.vstring("*")
    options['TnPHLTTagFilters']      = cms.vstring("*")
    options['TnPHLTProbeFilters']    = cms.vstring()
    options['HLTFILTERTOMEASURE']    = cms.vstring("")
    options['GLOBALTAG']             = 'MCRUN2_74_V9'
    options['PILEUPMC']              = '74X_mcRun2_asymptotic_v2'
    options['EVENTSToPROCESS']       = cms.untracked.VEventRange()
    options['MAXEVENTS']             = cms.untracked.int32(10000) 
else:
    options['INPUT_FILE_NAME']       = ("file:/tmp/meridian/SingleEleMicroAOD.root")
    options['OUTPUT_FILE_NAME']      = "TnPTree_data.root"
    options['TnPPATHS']              = ["HLT_Ele27_eta2p1_WPLoose_Gsf_v*"]
    options['TnPHLTTagFilters']      = cms.vstring("hltEle27WPLooseGsfTrackIsoFilter")
    options['TnPHLTProbeFilters']    = cms.vstring("")
    options['HLTFILTERTOMEASURE']    = cms.vstring("")
    options['GLOBALTAG']             = 'MCRUN2_74_V9'
    options['EVENTSToPROCESS']       = cms.untracked.VEventRange()

###################################################################

setModules(process, options)
from flashgg.Validation.treeContentPhotons_0T_cfi import *

process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff")
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.GlobalTag.globaltag = options['GLOBALTAG']

process.load('FWCore.MessageService.MessageLogger_cfi')
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

process.MessageLogger.cerr.threshold = ''
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(options['INPUT_FILE_NAME']),
                            eventsToProcess = options['EVENTSToPROCESS']
                            )

process.maxEvents = cms.untracked.PSet( input = options['MAXEVENTS'])

###################################################################
## ID
###################################################################

from PhysicsTools.TagAndProbe.photonIDModules_cfi import *
setIDs(process, options)

###################################################################
## PILE-UP
###################################################################

if (varOptions.isMC):
    process.load("PhysicsTools.TagAndProbe.pileupConfiguration_cfi")
    from PhysicsTools.TagAndProbe.pileupConfiguration_cfi import *
    process.pileupProducer.PileupMC = cms.vdouble(pu_distribs[options["PILEUPMC"]])

from PhysicsTools.TagAndProbe.photonIDModules_cfi import *

###################################################################
## SEQUENCES
###################################################################

process.egmPhotonIDs.physicsObjectSrc = cms.InputTag("photonFromDiPhotons")

process.pho_sequence = cms.Sequence(
    process.goodPhotonTags +
    process.goodPhotonProbes +
    process.goodPhotonProbesSelection +
    process.goodPhotonProbesEleSelection +
    process.goodPhotonsTagHLT +
    process.goodPhotonsProbeHLT +
    process.goodPhotonProbesL1
    )

###################################################################
## TnP PAIRS
###################################################################

process.allTagsAndProbes = cms.Sequence()
process.allTagsAndProbes *= process.tagTightRECO

process.mc_sequence = cms.Sequence()

if (varOptions.isMC):
    process.mc_sequence *= (process.McMatchTag + process.McMatchRECO)

##########################################################################
## TREE MAKER OPTIONS
##########################################################################
if (not varOptions.isMC):
    mcTruthCommonStuff = cms.PSet(
        isMC = cms.bool(False)
        )
    
process.PhotonToRECO = cms.EDAnalyzer("TagProbeFitTreeProducer",
                                      mcTruthCommonStuff, CommonStuffForPhotonProbe,
                                      tagProbePairs = cms.InputTag("tagTightRECO"),
                                      arbitration   = cms.string("None"),
                                      flags         = cms.PSet(
        #        passingPresel  = cms.InputTag("goodPhotonProbesPreselection"),
        #        passingIDMVA   = cms.InputTag("goodPhotonProbesIDMVA"),
        passingSel  = cms.InputTag("goodPhotonProbesSelection"),
        passingEleSel  = cms.InputTag("goodPhotonProbesEleSelection"),
        ),                                               
                                      allProbes     = cms.InputTag("goodPhotonsProbeHLT"),
                                      )

if (varOptions.isMC):
    process.PhotonToRECO.probeMatches  = cms.InputTag("McMatchRECO")
    process.PhotonToRECO.eventWeight   = cms.InputTag("generator")
    process.PhotonToRECO.PUWeightSrc   = cms.InputTag("pileupProducer","pileupWeights")
    process.PhotonToRECO.variables.Pho_dRTau  = cms.InputTag("GsfDRToNearestTauProbe")
    process.PhotonToRECO.tagVariables.probe_dRTau    = cms.InputTag("GsfDRToNearestTauProbe")

process.tree_sequence = cms.Sequence(process.PhotonToRECO)

##########################################################################
## PATHS
##########################################################################

process.out = cms.OutputModule("PoolOutputModule", 
                               fileName = cms.untracked.string(options['OUTPUTEDMFILENAME']),
                               SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring("p"))
                               )
process.outpath = cms.EndPath(process.out)
if (not options['DEBUG']):
    process.outpath.remove(process.out)

##########################################################################################
###### MICROAOD STUFF
##########################################################################################

process.load("flashgg/Taggers/flashggDiPhotonMVA_cfi")
process.flashggDiPhotonMVA.DiPhotonTag = cms.InputTag('flashggDiPhotons')


if (varOptions.isMC):
    process.p = cms.Path(
        process.flashggDiPhotonMVA +
        process.sampleInfo +
        process.hltFilter +
        process.pho_sequence + 
        process.allTagsAndProbes +
        process.pileupProducer +
        process.mc_sequence + 
        process.GsfDRToNearestTauProbe + 
        process.GsfDRToNearestTauTag + 
        process.tree_sequence
        )
else:
    process.p = cms.Path(
        process.flashggDiPhotonMVA +
        process.sampleInfo +
        process.hltFilter +
        process.pho_sequence + 
        process.allTagsAndProbes +
        process.mc_sequence +
        process.tree_sequence
        )

process.TFileService = cms.Service(
    "TFileService", fileName = cms.string(options['OUTPUT_FILE_NAME']),
    closeFileFast = cms.untracked.bool(True)
    )
