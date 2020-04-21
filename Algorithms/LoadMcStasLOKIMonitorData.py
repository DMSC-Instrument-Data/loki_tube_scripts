from mantid.kernel import *
from mantid.api import *
from mantid.simpleapi import *
import numpy


class LoadMcStasLOKIMonitorData(PythonAlgorithm):
    def PyInit(self):
        self.declareProperty(FileProperty(name="FOCMonitor", defaultValue="",
                                          action=FileAction.Load,
                                          extensions=["t"]), "Location of Geant4 data file for FOC Monitor")
        self.declareProperty(FileProperty(name="HaloMonitor", defaultValue="",
                                          action=FileAction.Load,
                                          extensions=["t"]), "Location of Geant4 data file for Halo Monitor")
        self.declareProperty(FileProperty(name="TransmissionMonitor", defaultValue="",
                                          action=FileAction.Load,
                                          extensions=["t"]), "Location of Geant4 data file for Transmission Monitor")

        self.declareProperty(FileProperty(name="LOKIIDF", defaultValue="",
                                          action=FileAction.Load,
                                          extensions=["xml"]),
                             "LOKI Instrument definition which contains monitors for data loading.")
        self.declareProperty(MatrixWorkspaceProperty("OutputWorkspace", "MonitorData", Direction.Output),
                             "Output workspace")

    def category(self):
        return 'ESS'

    def _extractData(self, filename):
        with open(filename) as monitorFile:
            data = monitorFile.readlines()
            header = data[35].split(" ")

            monitorData = numpy.array([x.split(" ") for x in data[36:-1]])

            wavelength = None
            tof = None
            if header[2] is 't':
                tof = monitorData[:, 0].astype(numpy.float32) * 1000000  # convert to microseconds
            else:
                wavelength = monitorData[:, 0].astype(numpy.float32)
            intensity = monitorData[:, 1].astype(numpy.float32)
            error = monitorData[:, 2].astype(numpy.float32)

            return tof, wavelength, intensity, error

    def _loadMonitorData(self, fileList, instFile):
        X = []
        Y = []
        E = []
        detIDs = []
        for i, file in enumerate(fileList):
            tof, wavelength, y, e = self._extractData(file)
            X.append(wavelength if tof is None else tof)
            Y.append(y)
            E.append(e)
            # x = convertToBinEdges(x)
            # monitors[i] = CreateWorkspace(OutputWorkspace="monitorWs"+str(i),DataX=x, DataY=y, DataE=e, NSpec=1)
            # monitors.append(x, y, e)
        X = numpy.array(X)
        Y = numpy.array(Y)
        E = numpy.array(E)
        ws = CreateWorkspace(OutputWorkspace="ws", DataX=X, DataY=Y, DataE=E, NSpec=len(fileList), UnitX='TOF',
                             YUnitLabel='Counts')

        LoadInstrument(Workspace=ws, Filename=instFile, RewriteSpectraMap=True)
        self.setProperty("OutputWorkspace", ws)
        DeleteWorkspace(Workspace=ws)

    def PyExec(self):
        foc = self.getProperty("FOCMonitor").value
        halo = self.getProperty("HaloMonitor").value
        trans = self.getProperty("TransmissionMonitor").value
        idf = self.getProperty("LOKIIDF").value

        self._loadMonitorData([foc, halo, trans], idf)


# Register algorithm with Mantid
AlgorithmFactory.subscribe(LoadMcStasLOKIMonitorData)
