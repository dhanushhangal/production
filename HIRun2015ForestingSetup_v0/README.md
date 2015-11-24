# HIRun2015 Express Forest 

First iteration setup. 

Setup environment:
```bash
cmsrel CMSSW_7_5_5_patch4
cd CMSSW_7_5_5_patch4/src
cmsenv
# Main forest
git cms-merge-topic -u CmsHI:forest_$CMSSW_VERSION
# RCT unpacker
git clone git@github.com:richard-cms/L1UpgradeAnalyzer.git Analyzers/L1UpgradeAnalyzer
# Dfinder
git clone -b Dfinder https://github.com/taweiXcms/Bfinder.git
git clone git@github.com:velicanu/production.git
scram build -j8

# grab submit scripts
cp production/HIRun2015ForestingSetup_v0/* .
```

Run interactively:
```bash
cmsRun runOpenHLT_pp_DATA_75X_Express.py outputFile=openHLT.root maxEvents=10 inputFiles=/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/163/00000/C4717393-ED8E-E511-9F65-02163E0120F9.root

cmsRun runForest_pp_DATA_75X_Express.py outputFile=test.root maxEvents=10 inputFiles=/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/163/00000/C4717393-ED8E-E511-9F65-02163E0120F9.root
```

Submit one run to caf queue
```bash
python submitOpenHLTExpress.py -q cmscaf1nd -o /store/group/phys_heavyions/velicanu/openhlt/Run2015E/ExpressPhysics/FEVT/ -i ExpressPhysics.262163.v2.list

python submitForestExpress.py -q cmscaf1nd -o /store/group/phys_heavyions/velicanu/forest/Run2015E/ExpressPhysics/FEVT/v2/ -i ExpressPhysics.262163.v2.list --proxy=proxyforprod
```

Submit all runs in 'runstoprocess' to caf queue
```bash
./suballruns.sh v6
```

