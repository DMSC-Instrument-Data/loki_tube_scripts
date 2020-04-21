from mantid.kernel import *
from mantid.api import *
from mantid.simpleapi import *


class LoadAndProcessGeant4ESS(PythonAlgorithm):
    def PyInit(self):
        self.declareProperty(FloatArrayProperty(name="BinParams"), "TOF binning parameters [min,width,max]")
        self.declareProperty(MatrixWorkspaceProperty("OutputWorkspace", "LOKIData", Direction.Output),
                             "Output workspace")
        self.declareProperty("SaveNexus", False, "Will save nexus file after processing if set to True.")

    def category(self):
        return 'ESS'

    def PyExec(self):
        geant4Alg = LoadGeant4AsciiFilesDialog()
        idf = geant4Alg.getProperty("IDF").value

        monitorAlg = LoadMcStasLOKIMonitorDataDialog(LOKIIDF=idf)

        params = self.getProperty("BinParams").value()

        dataWs = geant4Alg.getProperty("OutputWorkspace").value
        monitorWs = monitorAlg.getProperty("OutputWorkspace").value

        Rebin(InputWorkspace=dataWs, OutputWorkspace=dataWs, Params=params, PreserveEvents=False)
        Rebin(InputWorkspace=monitorWs, OutputWorkspace=monitorWs, Params=params, PreserveEvents=False)

        for i in range(3):
            dataWs.setY(i, monitorWs.readY(i))

        doSave = self.getProperty("SaveNexus").value
        self.setProperty("OutputWorkspace", dataWs)

        if doSave:
            SaveNexusDialog(dataWs)


# Register algorithm with Mantid
AlgorithmFactory.subscribe(LoadAndProcessGeant4ESS)
