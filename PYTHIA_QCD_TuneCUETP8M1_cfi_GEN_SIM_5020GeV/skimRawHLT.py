import FWCore.ParameterSet.Config as cms

process = cms.Process("RAWSkim")

# import of standard configurations
process.load("Configuration.StandardSequences.Services_cff")
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.load("Configuration.StandardSequences.ReconstructionHeavyIons_cff")
process.load("Configuration.StandardSequences.GeometryDB_cff")
process.load("Configuration.StandardSequences.MagneticField_38T_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load('Configuration.EventContent.EventContentHeavyIons_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.options = cms.untracked.PSet(
    #wantSummary = cms.untracked.bool(True)
)

#process.Timing = cms.Service("Timing")

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
    #'/store/hidata/HIRun2010/HIAllPhysics/RECO/ZS-v2/0033/7E0F627F-5C43-E011-AF82-003048F1CA12.root'
    #'file:/d101/icali/ROOTFiles_SWsrc392pa5/3855C0DE-FCF4-DF11-857D-003048D2C092.root'
    #'/store/hidata/HIRun2010/HIAllPhysics/RAW/v1/000/151/878/FCB5F9D9-16F5-DF11-89B1-001D09F251FE.root'
    '/store/user/dgulhan/PYTHIA_QCD_TuneCUETP8M1_cfi_GEN_SIM_5020GeV/Pythia8_Dijet15_pp_TuneCUETP8M1_Hydjet_MinBias_5020GeV_DIGIRAW_757p1_PrivMC_v2/151209_160122/0000/step2_1.root'
))


# Other statements
# process.GlobalTag.globaltag = "75X_mcRun2_HeavyIon_v11"
process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '75X_mcRun2_HeavyIon_v11', '')

process.load("HLTrigger.HLTfilters.hltHighLevel_cfi")

### PhotonHI SD
# process.hltJet55 = process.hltHighLevel.clone(HLTPaths = ['HLT_HISinglePhoton20_v*','HLT_HISinglePhoton30_v*'])
process.hltJet55 = process.hltHighLevel.clone(HLTPaths = ['HLT_HIL1Centralityext70100MinimumumBiasHF1AND_v1'])
# process.hltJet55 = process.hltHighLevel.clone(HLTPaths = ['L1_Centrality_ext0_5_MinimumumBiasHF1_AND'])
process.filterJet55 = cms.Path(process.hltJet55)



############ Output Modules ##########


### PhotonHI SD
process.outputSdJet55 = cms.OutputModule("PoolOutputModule",
                                            SelectEvents = cms.untracked.PSet(
    SelectEvents = cms.vstring('filterJet55')),
                                            dataset = cms.untracked.PSet(
    dataTier = cms.untracked.string('RAW'),
    filterName = cms.untracked.string('SD_HIJet55')),
                                            # outputCommands = process.RAWEventContent.outputCommands,
                                            outputCommands = process.FEVTDEBUGHLTEventContent.outputCommands,
                                            fileName = cms.untracked.string('step2.root')
                                            )

myEvContent = cms.PSet(
    outputCommands = cms.untracked.vstring('drop *_*_*_RAWSkim')
    )

process.outputSdJet55.outputCommands.extend(myEvContent.outputCommands)

process.this_is_the_end = cms.EndPath(
    process.outputSdJet55
)
