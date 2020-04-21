# Binning Parameters
params = [10000,300,100000]

# Default output names for workspaces.
geantWs = "Geant4Data"
monitorWs = "MonitorData"

# Launch dialog for loading Geant4 files
geant4Alg = LoadGeant4AsciiFilesDialog(OutputWorkspace=geantWs, Enable="OutputWorkspace")
idf = geant4Alg.getProperty("IDF").value

monitorAlg = LoadMcStasLOKIMonitorDataDialog(OutputWorkspace=monitorWs, LOKIIDF=idf)

Rebin(InputWorkspace=geantWs, OutputWorkspace=geantWs, Params=params, PreserveEvents=False)
Rebin(InputWorkspace=monitorWs, OutputWorkspace=monitorWs, Params=params, PreserveEvents=False)

gw = mtd[geantWs]
mw = mtd[monitorWs]


for i in range(3):
    gw.setY(i, mw.readY(i))
