import FWCore.ParameterSet.Config as cms

def setModules(process, options):

    process.sampleInfo = cms.EDProducer("tnp::SampleInfoTree",
                                        vertexCollection = cms.InputTag("offlineSlimmedPrimaryVertices"),
                                        genInfo = cms.InputTag("generator")
                                        )

    from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
    process.hltFilter = hltHighLevel.clone()
    process.hltFilter.throw = cms.bool(True)
    process.hltFilter.HLTPaths = options['TnPPATHS']
        
    process.GsfDRToNearestTauProbe = cms.EDProducer("DeltaRNearestGenPComputer",
                                                    probes = cms.InputTag("goodPhotonProbes"),
                                                    objects = cms.InputTag('flashggPrunedGenParticles'),
                                                    objectSelection = cms.string("abs(pdgId)==15"),
                                                    )

    process.GsfDRToNearestTauTag = cms.EDProducer("DeltaRNearestGenPComputer",
                                                  probes = cms.InputTag("goodEleTags"),
                                                  objects = cms.InputTag('flashggPrunedGenParticles'),
                                                  objectSelection = cms.string("abs(pdgId)==15"),
                                                  )

    ###################################################################
    ## ELECTRON MODULES
    ###################################################################
    
    process.goodPhotonTagL1 = cms.EDProducer("FlashggPhotonL1CandProducer",
                                             inputs = cms.InputTag("goodEleTags"),
                                             isoObjects = cms.InputTag("goodEleTags"),
                                             nonIsoObjects = cms.InputTag(""),
                                             minET = cms.double(25),
                                             dRmatch = cms.double(0.2),
                                             isolatedOnly = cms.bool(False)
                                             )
    
    process.goodEleTags = cms.EDFilter("FlashggPhotonRefSelector",
                                          src = cms.InputTag(options['PHOTON_COLL']),
                                          cut = cms.string(options['ELE_TAG_CUTS'])
                                          )
    
    process.goodPhotonProbes = cms.EDFilter("FlashggPhotonRefSelector",
                                            src = cms.InputTag(options['PHOTON_COLL']),
                                            cut = cms.string(options['PHOTON_CUTS'])
                                            )
    
    ###################################################################
    

    process.goodPhotonProbesSelection = cms.EDFilter("FlashggPhotonRefSelector",
                                            src = cms.InputTag(options['PHOTON_COLL']),
                                            cut = cms.string(options['PHOTON_SEL_CUTS'])
                                            )

    process.goodPhotonProbesEleSelection = cms.EDFilter("FlashggPhotonRefSelector",
                                            src = cms.InputTag(options['PHOTON_COLL']),
                                            cut = cms.string(options['PHOTON_SEL_ELE_CUTS'])
                                            )

    process.goodPhotonProbesEleVetoSelection = cms.EDFilter("FlashggPhotonRefSelector",
                                            src = cms.InputTag(options['PHOTON_COLL']),
                                            cut = cms.string(options['PHOTON_SEL_ELE_VETO_CUTS'])
                                            )
    
    ###################################################################

    process.goodEleTagHLT = cms.EDProducer("FlashggPhotonTriggerCandProducer",
                                               filterNames = options['TnPHLTTagFilters'],
                                               inputs      = cms.InputTag("goodEleTags"),
                                               bits        = cms.InputTag('TriggerResults::HLT'),
                                               objects     = cms.InputTag('selectedPatTrigger'),
                                               dR          = cms.double(0.3),
                                               isAND       = cms.bool(True)
                                               )
    
    process.goodPhotonsProbeHLT = cms.EDProducer("FlashggPhotonTriggerCandProducer",
                                                 filterNames = options['TnPHLTProbeFilters'],
                                                 inputs      = cms.InputTag("goodPhotonProbes"),
                                                 bits        = cms.InputTag('TriggerResults::HLT'),
                                                 objects     = cms.InputTag('selectedPatTrigger'),
                                                 dR          = cms.double(0.3),
                                                 isAND       = cms.bool(True)
                                                 )
    
    process.goodPhotonProbesL1 = cms.EDProducer("FlashggPhotonL1CandProducer",
                                                inputs = cms.InputTag("goodPhotonProbes"),
                                                isoObjects = cms.InputTag("l1extraParticles:Isolated"),
                                                nonIsoObjects = cms.InputTag("l1extraParticles:NonIsolated"),
                                                minET = cms.double(40),
                                                dRmatch = cms.double(0.2),
                                                isolatedOnly = cms.bool(False)
                                                )
    
    ###################################################################
    ## PHOTON ISOLATION
    ###################################################################
    process.load("RecoEgamma/PhotonIdentification/PhotonIDValueMapProducer_cfi")

    process.goodDiEle = cms.EDProducer("CandViewShallowCloneCombiner",
#                                      decay = cms.string("goodPhotonsTagHLT goodPhotonsProbeHLT"), 
                                      decay = cms.string("goodEleTagHLT goodEleTags"), 
                                      checkCharge = cms.bool(False),
                                      cut = cms.string("35<mass<1000"),
                                      roles = cms.vstring('hltMatch', 'ele2')
                                      )

    process.tagTightRECO = cms.EDProducer("CandViewShallowCloneCombiner",
#                                      decay = cms.string("goodPhotonsTagHLT goodPhotonsProbeHLT"), 
                                      decay = cms.string("goodDiEle goodPhotonProbes"), 
                                      checkCharge = cms.bool(False),
                                      cut = cms.string("50<mass<1000"),
                                      )

    
    ###################################################################
    ## MC MATCHING
    ###################################################################

    process.McMatchTag = cms.EDProducer("MCTruthDeltaRMatcherNew",
                                        matchPDGId = cms.vint32(11),
                                        src = cms.InputTag("goodEleTags"),
                                        distMin = cms.double(0.2),
                                        matched = cms.InputTag("flashggPrunedGenParticles"),
                                        checkCharge = cms.bool(False)
                                        )
    
    process.McMatchRECO = cms.EDProducer("MCTruthDeltaRMatcherNew",
                                         matchPDGId = cms.vint32(11),
                                         src = cms.InputTag("goodPhotonProbes"),
                                         distMin = cms.double(0.2),
                                         matched = cms.InputTag("flashggPrunedGenParticles"),
                                         checkCharge = cms.bool(False)
                                         )
