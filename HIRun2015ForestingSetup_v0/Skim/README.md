## Skim data from trigger 

Setup the environment as for forest (up one level readme)

### Run interactively

```bash
cmsRun skimTriggersEventContent.py maxEvents=100 inputFiles=root://cms-xrd-global.cern.ch//eos/cms/store/group/phys_heavyions/velicanu/reco/HIPhysicsMinBiasUPC/v0/000/262/548/recoExpress_103.root outputFile=a
```

### Submit to cafqueue

```bash
# add --proxy=proxyforprod after you've ran this once and see a new proxyforprod file in your directory
python submitskimTriggersEventContent.py -q cmscaf1nd -o /store/group/phys_heavyions/velicanu/eventsize/HIPhysicsMinBiasUPC/v2/ -i HIPhysicsMinBiasUPC.262548.list 
```

## Make FEVT from RAW or .dat streamer

```bash
# for raw:
cmsRun RunExpressProcessingCfgonRAW.py outputFile=RAWRECO.root maxEvents=2 inputFiles=root://cms-xrd-global.cern.ch//eos/cms/tier0/store/hidata/HIRun2015/HIMinimumBias2/RAW/v1/000/262/640/00000/2001503F-3394-E511-AED3-02163E014160.root

# for streamer files:
cmsRun RunExpressProcessingCfg.py outputFile=RAWRECO.root maxEvents=100 inputFiles=root://cms-xrd-global.cern.ch//eos/cms/store/t0streamer/Data/HIPhysicsMinBiasUPC/000/262/548/run262548_ls0118_streamHIPhysicsMinBiasUPC_StorageManager.dat
```
