### HiForest Configuration
# Collisions: pp
# Type: MC
# Input: AOD

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing('analysis')
options.register ('isPP',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.bool,
                  "Flag if this is a pp simulation")
options.parseArguments()

import FWCore.ParameterSet.Config as cms
process = cms.Process('HiForest')
process.options = cms.untracked.PSet()

#####################################################################################
# HiForest labelling info
#####################################################################################

process.load("HeavyIonsAnalysis.JetAnalysis.HiForest_cff")
process.HiForest.inputLines = cms.vstring("HiForest V3",)
import subprocess
version = subprocess.Popen(["(cd $CMSSW_BASE/src && git describe --tags)"], stdout=subprocess.PIPE, shell=True).stdout.read()

if version == '':
    version = 'no git info'
process.HiForest.HiForestVersion = cms.string(version)

#####################################################################################
# Input source
#####################################################################################

process.source = cms.Source("PoolSource",
                            duplicateCheckMode = cms.untracked.string("noDuplicateCheck"),
                            fileNames = cms.untracked.vstring(options.inputFiles[0]
				#"/store/user/gsfs/ReggeGribovPartonMC_EposLHC_pPb_4080_4080/EPOS_MinBias_pPb_RECO25ns_10272016/161027_121447/0000/step3_25ns_RAW2DIGI_L1Reco_RECO_1.root"
                           #'/store/group/phys_heavyions/kjung/Pythia8Epos_RECOStep/pPb_Pythia8Epos_8TeV_HLT_pthat15/HIRun2016PA/crab_pPb_Pythia8Epos_8022Validation_RECO_pthat15/161102_015603/0000/pPb_Pythia8Epos_RECO_101.root'    
			#	'file:/afs/cern.ch/user/k/kjung/run2Validation/HLTchecks/CMSSW_8_0_22/src/pPb_5TeVEpos_RECO.root'
			#'/store/group/phys_heavyions/kjung/Epos5TeV_8022Valid_RECO/EPOS5TeV_GEN_SIM/crab_pPb_5TeVEpos_8022Validation_RECO/161104_192347/0000/pPb_5TeVEpos_RECO_1.root'	
			)
)

# Number of events we want to process, -1 = all events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents))


#####################################################################################
# Load Global Tag, Geometry, etc.
#####################################################################################

process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.Geometry.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load("CondCore.DBCommon.CondDBCommon_cfi")
 
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '80X_mcRun2_asymptotic_2016_miniAODv2_v1', '')
process.HiForest.GlobalTagLabel = process.GlobalTag.globaltag


# Customization
from HeavyIonsAnalysis.Configuration.CommonFunctions_cff import overrideJEC_pPb8TeV
process = overrideJEC_pPb8TeV(process)

process.GlobalTag.toGet.extend([
		cms.PSet(record = cms.string("HeavyIonRcd"),
			tag = cms.string("CentralityTable_HFtowersPlusTrunc200_EPOS8TeV_v80x01_mc"),
			#tag = cms.string("CentralityTable_HFtowersPlusTrunc200_EPOS5TeV_v80x01_mc"),
			connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS"),
			label = cms.untracked.string("HFtowersPlusTruncEpos")
			),
		cms.PSet(record = cms.string("L1TUtmTriggerMenuRcd"),
			tag = cms.string("L1Menu_HeavyIons2016_v2_m2_xml"),
			connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS")
			)
])


#####################################################################################
# Define tree output
#####################################################################################

process.TFileService = cms.Service("TFileService",
                                   fileName=cms.string(options.outputFile))

#####################################################################################
# Additional Reconstruction and Analysis: Main Body
#####################################################################################

####################################################################################

#############################
# Jets
#############################

process.load("HeavyIonsAnalysis.JetAnalysis.FullJetSequence_JECPPb")
# Use this version for JEC
#process.load("HeavyIonsAnalysis.JetAnalysis.FullJetSequence_JECPP")

#####################################################################################

############################
# Event Analysis
############################

## temporary centrality bin
process.load("RecoHI.HiCentralityAlgos.CentralityBin_cfi")
process.centralityBin.Centrality = cms.InputTag("pACentrality")
process.centralityBin.centralityVariable = cms.string("HFtowersPlusTrunc")
#process.centralityBin.nonDefaultGlauberModel = cms.string("Hydjet_Drum")
process.centralityBin.nonDefaultGlauberModel = cms.string("Epos")

process.load('HeavyIonsAnalysis.EventAnalysis.hltanalysis_cff')
process.hltanalysis.getPrescales = cms.untracked.bool(False)
process.load('HeavyIonsAnalysis.EventAnalysis.hltobject_pPb_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.hievtanalyzer_data_cfi') #use data version to avoid PbPb MC
process.hiEvtAnalyzer.Vertex = cms.InputTag("offlinePrimaryVertices")
process.hiEvtAnalyzer.doCentrality = cms.bool(False)
process.hiEvtAnalyzer.CentralitySrc = cms.InputTag("pACentrality")
process.hiEvtAnalyzer.CentralityBinSrc = cms.InputTag("centralityBin","HFtowersPlusTrunc")
process.hiEvtAnalyzer.doEvtPlane = cms.bool(False)
process.hiEvtAnalyzer.doMC = cms.bool(True) #general MC info
process.hiEvtAnalyzer.doHiMC = cms.bool(False) #HI specific MC info

process.load('HeavyIonsAnalysis.JetAnalysis.HiGenAnalyzer_cfi')
process.HiGenParticleAna.genParticleSrc = cms.untracked.InputTag("genParticles")
process.HiGenParticleAna.doHI = False
process.load('HeavyIonsAnalysis.EventAnalysis.runanalyzer_cff')
process.load("HeavyIonsAnalysis.JetAnalysis.pfcandAnalyzer_pp_cfi")
process.pfcandAnalyzer.skipCharged = False
process.pfcandAnalyzer.pfPtMin = 0
process.pfcandAnalyzer.pfCandidateLabel = cms.InputTag("particleFlow")
process.pfcandAnalyzer.doVS = cms.untracked.bool(False)
process.pfcandAnalyzer.doUEraw_ = cms.untracked.bool(False)
process.pfcandAnalyzer.genLabel = cms.InputTag("genParticles")

#####################################################################################

#########################
# Track Analyzer
#########################
process.load('HeavyIonsAnalysis.JetAnalysis.ExtraTrackReco_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.TrkAnalyzers_cff')

# Use this instead for track corrections
## process.load('HeavyIonsAnalysis.JetAnalysis.TrkAnalyzers_Corr_cff')

#####################################################################################

#####################
# photons
######################
process.load('HeavyIonsAnalysis.PhotonAnalysis.ggHiNtuplizer_cfi')
process.ggHiNtuplizer.gsfElectronLabel   = cms.InputTag("gedGsfElectrons")
process.ggHiNtuplizer.recoPhotonHiIsolationMap = cms.InputTag('photonIsolationHIProducerpp')
process.ggHiNtuplizer.VtxLabel           = cms.InputTag("offlinePrimaryVertices")
process.ggHiNtuplizer.particleFlowCollection = cms.InputTag("particleFlow")
process.ggHiNtuplizer.doVsIso            = cms.bool(False)
process.ggHiNtuplizer.doElectronVID      = cms.bool(True)
process.ggHiNtuplizerGED = process.ggHiNtuplizer.clone(recoPhotonSrc = cms.InputTag('gedPhotons'),
                                                       recoPhotonHiIsolationMap = cms.InputTag('photonIsolationHIProducerppGED'))

####################################################################################
#####################
# Electron ID
#####################

from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
# turn on VID producer, indicate data format to be processed
# DataFormat.AOD or DataFormat.MiniAOD
dataFormat = DataFormat.AOD
switchOnVIDElectronIdProducer(process, dataFormat)

# define which IDs we want to produce. Check here https://twiki.cern.ch/twiki/bin/viewauth/CMS/CutBasedElectronIdentificationRun2#Recipe_for_regular_users_for_7_4
my_id_modules = ['RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Spring15_25ns_V1_cff']

#add them to the VID producer
for idmod in my_id_modules:
    setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)
#####################################################################################
#####################
# Rechit analyzer
#####################
process.load('HeavyIonsAnalysis.JetAnalysis.rechitanalyzer_pp_cfi')
process.rechitanalyzer.doVS = cms.untracked.bool(False)
process.rechitanalyzer.doEcal = cms.untracked.bool(False)
process.rechitanalyzer.doHcal = cms.untracked.bool(False)
process.rechitanalyzer.doHF = cms.untracked.bool(False)
process.rechitanalyzer.JetSrc = cms.untracked.InputTag("ak4CaloJets")
process.pfTowers.JetSrc = cms.untracked.InputTag("ak4CaloJets")

#####################
# New rho analyzer
#####################
process.load('HeavyIonsAnalysis.JetAnalysis.hiFJRhoAnalyzer_cff')

#####################
## Event Plane
####################

process.load('RecoHI.HiEvtPlaneAlgos.HiEvtPlane_cfi')
process.hiEvtPlane.vertexTag = cms.InputTag ("offlinePrimaryVertices")
process.hiEvtPlane.trackTag = cms.InputTag("generalTracks")
process.hiEvtPlane.centralityVariable= cms.string("HFtowersPlusTrunc")
process.hiEvtPlane.loadDB = cms.bool(False)
process.hiEvtAnalyzer.doEvtPlane = cms.bool(True)

#####################
# Muon Analyzer
#####################
process.load('HeavyIonsAnalysis.MuonAnalysis.hltMuTree_cfi')
process.hltMuTree.vertices = cms.InputTag("offlinePrimaryVertices")
process.hltMuTree.genparticle = cms.InputTag("genParticles")

#########################
# Main analysis list
#########################
process.ana_step = cms.Path(process.hltanalysis *
			    process.hltobject *
                            #process.centralityBin *
			    process.hiEvtAnalyzer *
                            process.HiGenParticleAna*
                            process.jetSequences +
                            process.egmGsfElectronIDSequence + #Should be added in the path for VID module
                            process.ggHiNtuplizer +
                            process.ggHiNtuplizerGED +
                            #process.hiFJRhoAnalyzer +
			    process.pfcandAnalyzer +
			    process.hiEvtPlane +
			    process.hltMuTree +
                            process.HiForest +
			    process.trackSequencesPP +
                            process.runAnalyzer +
                            process.rechitanalyzer
)

#####################################################################################

#########################
# Event Selection
#########################

process.load('HeavyIonsAnalysis.JetAnalysis.EventSelection_cff')
process.pHBHENoiseFilterResultProducer = cms.Path( process.HBHENoiseFilterResultProducer )
process.HBHENoiseFilterResult = cms.Path(process.fHBHENoiseFilterResult)
process.HBHENoiseFilterResultRun1 = cms.Path(process.fHBHENoiseFilterResultRun1)
process.HBHENoiseFilterResultRun2Loose = cms.Path(process.fHBHENoiseFilterResultRun2Loose)
process.HBHENoiseFilterResultRun2Tight = cms.Path(process.fHBHENoiseFilterResultRun2Tight)
process.HBHEIsoNoiseFilterResult = cms.Path(process.fHBHEIsoNoiseFilterResult)

process.PAprimaryVertexFilter = cms.EDFilter("VertexSelector",
    src = cms.InputTag("offlinePrimaryVertices"),
    cut = cms.string("!isFake && abs(z) <= 25 && position.Rho <= 2 && tracksSize >= 2"),
    filter = cms.bool(True), # otherwise it won't filter the events
)

process.NoScraping = cms.EDFilter("FilterOutScraping",
 applyfilter = cms.untracked.bool(True),
 debugOn = cms.untracked.bool(False),
 numtrack = cms.untracked.uint32(10),
 thresh = cms.untracked.double(0.25)
)

process.pPAprimaryVertexFilter = cms.Path(process.PAprimaryVertexFilter)
process.pBeamScrapingFilter=cms.Path(process.NoScraping)

process.load("HeavyIonsAnalysis.VertexAnalysis.PAPileUpVertexFilter_cff")

process.pVertexFilterCutG = cms.Path(process.pileupVertexFilterCutG)
process.pVertexFilterCutGloose = cms.Path(process.pileupVertexFilterCutGloose)
process.pVertexFilterCutGtight = cms.Path(process.pileupVertexFilterCutGtight)
process.pVertexFilterCutGplus = cms.Path(process.pileupVertexFilterCutGplus)
process.pVertexFilterCutE = cms.Path(process.pileupVertexFilterCutE)
process.pVertexFilterCutEandG = cms.Path(process.pileupVertexFilterCutEandG)

process.load('HeavyIonsAnalysis.Configuration.hfCoincFilter_cff')
process.phfCoincFilter1 = cms.Path(process.hfCoincFilter)
process.phfCoincFilter2 = cms.Path(process.hfCoincFilter2)
process.phfCoincFilter3 = cms.Path(process.hfCoincFilter3)
process.phfCoincFilter4 = cms.Path(process.hfCoincFilter4)
process.phfCoincFilter5 = cms.Path(process.hfCoincFilter5)

process.pAna = cms.EndPath(process.skimanalysis)

# Customization
