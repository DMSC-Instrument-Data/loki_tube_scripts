from mantid.kernel import *
from mantid.api import *
from mantid.simpleapi import *
from mantid.dataobjects import EventWorkspaceProperty
import numpy
import datetime
import csv


class LoadGeant4AsciiFiles(PythonAlgorithm):
    OUTPUT_NAME = "Geant4EventData"

    def PyInit(self):
        self.declareProperty(FileProperty(name="Geant4File", defaultValue="",
                                          action=FileAction.Load,
                                          extensions=["out"]), "Location of Geant4 data file")
        self.declareProperty(FileProperty(name="IDF", defaultValue="",
                                          action=FileAction.Load,
                                          extensions=["xml"]), "IDF corresponding to instrument.")
        self.declareProperty(FileProperty(name="ComplexToSimpleIDMap", defaultValue="",
                                          action=FileAction.Load,
                                          extensions=["csv"]),
                             "CSV file containing map between complex (Geant4) and simple (Mantid) detector wiring.")
        self.declareProperty(EventWorkspaceProperty("OutputWorkspace", self.OUTPUT_NAME, Direction.Output),
                             "Output event workspace")

    def category(self):
        return 'ESS'

    def _loadGeant4Data(self, filename):
        progReporter = Progress(self, start=0.0, end=1.0,
                                nreports=1)
        progReporter.reportIncrement(1, "Loading Geant4 data.")
        with open(filename) as csvfile:
            lokidata_csv = list(csv.reader(csvfile, delimiter=" ", lineterminator='\r', skipinitialspace=True))
            for i in range(5):
                del lokidata_csv[:1]
            lokidata = numpy.array(lokidata_csv)

        tof = lokidata[:, 9].astype(float)  # milliseconds
        weights = lokidata[:, 10].astype(float)  # weight
        tof = tof * 1000.0  # convert to microseconds
        detids = [int(x, 16) for x in lokidata[:, -1]]
        detids = numpy.array(detids).astype(numpy.long)
        return tof, detids, weights

    def _loadEmptyInstrument(self, idf):
        return LoadEmptyInstrument(idf, MakeEventWorkspace=True)

    def _loadIDConversionMap(self, filename):
        with open(filename) as convCsvFile:
            convData = list(csv.reader(convCsvFile, delimiter=","))
            convData = numpy.array(convData)

            consStart = convData[:, 0].astype(numpy.long)
            consEnd = convData[:, 1].astype(numpy.long)
            start = convData[:, 2].astype(numpy.long)
            end = convData[:, 3].astype(numpy.long)

            convMap = {}
            for cs, ce, s, e in zip(consStart, consEnd, start, end):
                # add 1 to end of range as range is not inclusive of last value
                convMap.update(zip(range(s, e + 1), range(cs, ce + 1)))

        return convMap

    def _getDetToIndexMap(self, wksp):
        numHists = wksp.getNumberHistograms()
        detIndexMap = {}
        for i in range(numHists):
            eventList = wksp.getSpectrum(i)
            id = eventList.getDetectorIDs()
            detIndexMap[id[0]] = i
            eventList.clear(False)

        return detIndexMap

    def _rebinAndAddAxesLabels(self, wksp):
        tofmin = int(wksp.getTofMin())
        tofmax = int(wksp.getTofMax())
        width = tofmax - tofmin
        ptMin = wksp.getPulseTimeMin()
        ptMax = wksp.getPulseTimeMax()

        run = wksp.run()
        run.setStartAndEndTime(ptMin, ptMax)
        run.addProperty("run_number", "1", True)
        run.addProperty("run_start", str(ptMin), True)
        run.addProperty("TimeUnit", "Micro Seconds", True)
        SortEvents(InputWorkspace=wksp, SortBy='Pulse Time')
        wksp = Rebin(InputWorkspace=wksp, OutputWorkspace=wksp,
                     Params=str(tofmin) + "," + str(width) + "," + str(tofmax), PreserveEvents=True)
        wksp.setYUnitLabel("Counts")
        wksp.getAxis(0).setUnit("TOF")

    def _addEventsToWorkspace(self, Geant4Data, idConvMap, tof, detids, weights):
        detToIndex = self._getDetToIndexMap(Geant4Data)
        pulsetime = datetime.datetime.now()
        progReporter = Progress(self, start=0.0, end=1.0,
                                nreports=tof.size)
        for i in range(tof.size):
            progReporter.reportIncrement(1, "Writing Geant4 events to workspace.")
            try:
                id = idConvMap[detids[i]]
                listIndex = detToIndex[id]
                eventList = Geant4Data.getSpectrum(listIndex)
                eventList.switchTo(EventType.WEIGHTED)
                eventList.addWeightedEventQuickly(tof[i], weights[i], 0, DateAndTime(pulsetime.isoformat(sep="T")))
            except:
                pass

        progReporter = Progress(self, start=0.0, end=1.0,
                                nreports=1)
        progReporter.reportIncrement(1, "Sorting events and rebinning to min and max TOF.")
        self._rebinAndAddAxesLabels(Geant4Data)
        self.setProperty("OutputWorkspace", Geant4Data)

    def PyExec(self):
        filename = self.getProperty("Geant4File").value
        tof, detids, weights = self._loadGeant4Data(filename)
        idf = self.getProperty("IDF").value
        simpleToComplexIDMap = self.getProperty("ComplexToSimpleIDMap").value

        emptyWorkspace = self._loadEmptyInstrument(idf)
        idConvMap = self._loadIDConversionMap(simpleToComplexIDMap)

        self._addEventsToWorkspace(emptyWorkspace, idConvMap, tof, detids, weights)


# Register algorithm with Mantid
AlgorithmFactory.subscribe(LoadGeant4AsciiFiles)
