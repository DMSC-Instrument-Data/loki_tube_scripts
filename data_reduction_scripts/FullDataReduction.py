from mantid.simpleapi import *


class LokiSANSTestReduction:
    sampleHolder = 'some-sample-holder'
    detectorBench = 'DetectorBench'
    maskingCylinderXML = \
        """
        <infinite-cylinder id="beam_stop">
            <centre x="0" y="0" z="0.0" />
            <axis x="0" y="0" z="1" />
            <radius val="0.045" />
        </infinite-cylinder><algebra val="beam_stop"/>
        """
    maskingPlaneXML = \
        """
        <infinite-plane id="unique phi_plane1">
                <point-in-plane x="0" y="0" z="0" />
                <normal-to-plane x="-1.0" y="-1.22464679915e-16" z="0" />
            </infinite-plane>
            <infinite-plane id="unique phi_plane2">
                <point-in-plane x="0" y="0" z="0" />
                <normal-to-plane x="-1.0" y="-2.44929359829e-16" z="0" />
            </infinite-plane>
            <infinite-plane id="unique phi_plane3">
                <point-in-plane x="0" y="0" z="0" />
                <normal-to-plane x="1.0" y="2.44929359829e-16" z="0" />
            </infinite-plane>
            <infinite-plane id="unique phi_plane4">
                <point-in-plane x="0" y="0" z="0" />
                <normal-to-plane x="1.0" y="1.22464679915e-16" z="0" />
            </infinite-plane>
            <algebra val="#((unique phi_plane1 unique phi_plane2):(unique phi_plane3 unique phi_plane4))" />
        """

    def __init__(self, instrumentDefinitionFile, detectorMaskFile, sampleRunNumber, sampleTransmissionRunNumber,
                 backgroundRunNumber, backgroundtransmissionRunNumber, directbeamtransmissionRunNumber, dataFolderPath,
                 directBeamFile, moderatorFile):
        self.idf = dataFolderPath + instrumentDefinitionFile
        self.maskFile = dataFolderPath + detectorMaskFile
        self.sampleRun = sampleRunNumber
        self.sampleTransRun = sampleTransmissionRunNumber
        self.backgroundRun = backgroundRunNumber
        self.backgroundTransRun = backgroundtransmissionRunNumber
        self.directBeamTransRun = directbeamtransmissionRunNumber
        self.dataFolder = dataFolderPath
        self.dbFile = dataFolderPath + directBeamFile
        self.modFile = dataFolderPath + moderatorFile

    def _moveSampleHolder(self, wsName, Z):
        MoveInstrumentComponent(Workspace=wsName, ComponentName=self.sampleHolder, Z=Z)

    def _moveDetectorBench(self, wsName, Y):
        MoveInstrumentComponent(Workspace=wsName, ComponentName=self.detectorBench, Y=Y)

    def _moveSampleHolderAndDetectorBench(self, wsName, sampleZ, benchY):
        self._moveSampleHolder(wsName, sampleZ)
        self._moveDetectorBench(wsName, benchY)

    def _load(self, runNumber, suffix):
        file = self.dataFolder + 'LARMOR000' + str(runNumber) + '.nxs'
        wsName = str(runNumber) + suffix
        Load(Filename=file, OutputWorkspace=wsName)
        return wsName

    def _loadSampleRun(self):
        self.sampleWsName = self._load(self.sampleRun, '_sans')
        return self.sampleWsName

    def _loadSampleTransmissionRun(self):
        self.sampleTransWsName = self._load(self.sampleTransRun, '_trans')
        return self.sampleTransWsName

    def _loadBackgroundRun(self):
        self.bgWsName = self._load(self.backgroundRun, '_bg_sans')
        return self.bgWsName

    def _loadBackgroundTransmissionRun(self):
        self.bgTransWsName = self._load(self.backgroundTransRun, '_bg_trans')
        return self.bgTransWsName

    # JH added this bit
    def _loadDirectBeamTransmissionRun(self):
        self.dbTransWsName = self._load(self.directBeamTransRun, '_db_trans')
        return self.dbTransWsName

    def _loadAllData(self):
        samplePosZ = 0.30530
        benchPosY = 0.001
        self._moveSampleHolderAndDetectorBench(self._loadSampleRun(), samplePosZ, benchPosY)
        self._moveSampleHolderAndDetectorBench(self._loadBackgroundRun(), samplePosZ, benchPosY)
        self._moveSampleHolderAndDetectorBench(self._loadSampleTransmissionRun(), samplePosZ, benchPosY)
        self._moveSampleHolderAndDetectorBench(self._loadBackgroundTransmissionRun(), samplePosZ, benchPosY)
        self._moveSampleHolderAndDetectorBench(self._loadDirectBeamTransmissionRun(), samplePosZ, benchPosY)

    def _applyMask(self, ws):
        ws = MaskBins(InputWorkspace=ws, InputWorkspaceIndexType='WorkspaceIndex', XMin=5, XMax=1500)
        ws = MaskBins(InputWorkspace=ws, InputWorkspaceIndexType='WorkspaceIndex', XMin=17500, XMax=19000)
        detectorMask = LoadMask(Instrument=self.idf, InputFile=self.maskFile)
        MaskDetectors(Workspace=ws, MaskedWorkspace=detectorMask)
        # each detector mask must be applied separately
        MaskDetectorsInShape(Workspace=ws, ShapeXML=self.maskingCylinderXML)
        MaskDetectorsInShape(Workspace=ws, ShapeXML=self.maskingPlaneXML)
        return ws

    def _setupBackground(self, wsName, outWsName):
        ws = ExtractSpectra(InputWorkspace=wsName, DetectorList='1,4')
        ws = CalculateFlatBackground(InputWorkspace=ws, StartX=40000, EndX=99000,
                                     WorkspaceIndexList='0', Mode='Mean')
        ws = CalculateFlatBackground(InputWorkspace=ws, StartX=88000, EndX=98000,
                                     WorkspaceIndexList='1', Mode='Mean')
        ws = ConvertUnits(InputWorkspace=ws, Target='Wavelength')
        ws = Rebin(InputWorkspace=ws, OutputWorkspace=outWsName, Params='0.9,-0.025,13.5')
        return mtd[outWsName]

    def _setupAndCalculateTransmission(self, wsName, outWsName):
        transWsTmp = self._setupBackground(wsName, "transWsTmp")
        dbTransWs = self._setupBackground(wsName, "dbTransWs")
        # setup direct beam transmission file
        CalculateTransmission(SampleRunWorkspace=transWsTmp,
                              DirectRunWorkspace=dbTransWs,
                              OutputWorkspace=outWsName,
                              IncidentBeamMonitor=1,
                              TransmissionMonitor=4, RebinParams='0.9,-0.025,13.5',
                              FitMethod='Polynomial',
                              PolynomialOrder=3, OutputUnfittedData=True)
        return mtd[outWsName]

    def _reductionQ1D(self, wsName, transWsName, outWsName):
        transWs = self._setupAndCalculateTransmission(transWsName, "transWs")
        dataWs = CloneWorkspace(InputWorkspace=wsName)
        # monitor workspace needs to be extracted before masking occurs.
        monWs = ExtractSingleSpectrum(InputWorkspace=dataWs, WorkspaceIndex=0)
        dataWs = self._applyMask(dataWs)
        dataWs = ConvertUnits(InputWorkspace=dataWs, Target='Wavelength')
        dataWs = Rebin(InputWorkspace=dataWs, Params='0.9,-0.025,13.5')

        monWs = CalculateFlatBackground(InputWorkspace=monWs, StartX=40000, EndX=99000, Mode='Mean')
        monWs = ConvertUnits(InputWorkspace=monWs, Target='Wavelength')
        monWs = Rebin(monWs, Params='0.9,-0.025,13.5')

        # this factor seems to be a fudge factor. Explanation pending.
        factor = 100.0 / 176.71458676442586
        valWs = CreateSingleValuedWorkspace(DataValue=factor)
        dataWs = Multiply(LHSWorkspace=dataWs, RHSWorkspace=valWs)

        # Setup direct beam and normalise to monitor. I.e. adjust for efficiency of detector across the wavelengths.
        dbWs = LoadRKH(Filename=self.dbFile)
        dbWs = ConvertToHistogram(InputWorkspace=dbWs)
        dbWs = RebinToWorkspace(WorkspaceToRebin=dbWs, WorkspaceToMatch=dataWs)
        dbWs = Multiply(LHSWorkspace=monWs, RHSWorkspace=dbWs)
        dbWs = Multiply(LHSWorkspace=transWs, RHSWorkspace=dbWs)

        # Estimate qresolution function
        modWs = LoadRKH(Filename=self.modFile)
        modWs = ConvertToHistogram(InputWorkspace=modWs)
        qResWs = TOFSANSResolutionByPixel(InputWorkspace=dataWs,
                                          DeltaR=8,
                                          SampleApertureRadius=4.0824829046386295,
                                          SourceApertureRadius=14.433756729740645,
                                          SigmaModerator=modWs, CollimationLength=5,
                                          AccountForGravity=True,
                                          ExtraLength=2)

        Q1D(DetBankWorkspace=dataWs, OutputWorkspace=outWsName, OutputBinning='0.0045,-0.08,0.7',
            WavelengthAdj=dbWs, AccountForGravity=True, ExtraLength=2, QResolution=qResWs)

        return mtd[outWsName]

    def _reduce(self):
        # reduce sample
        sampleQ1d = self._reductionQ1D(self.sampleWsName, self.sampleTransWsName, "sampleQ1d")
        # reduce sample can (background)
        bgQ1d = self._reductionQ1D(self.bgWsName, self.bgTransWsName, "bgQ1d")

        # subtract reduced background from reduced sample
        reduced = Minus(LHSWorkspace=sampleQ1d, RHSWorkspace=bgQ1d)
        reduced = CropWorkspace(InputWorkspace=reduced, XMin=0.008, XMax=0.6)  # ToDo make parameters.

        # add log
        AddSampleLog(Workspace=reduced, LogName='UserFile',
                     LogText='USER_Raspino_191E_BCSLarmor_24Feb2020_v1.txt')
        AddSampleLog(Workspace=reduced, LogName='Transmission',
                     LogText=str(self.sampleTransRun) + '_trans_sample_0.9_13.5_unfitted')
        AddSampleLog(Workspace="transWs", LogName='TransmissionCan',
                     LogText='49335_trans_can_0.9_13.5_unfitted')

    def execute(self):
        self._loadAllData()
        self._reduce()


if __name__ == "__main__":
    dataFolder = '/Users/judithhouston/Documents/ESS/LoKi/Design_documents/Detector/LarmorDec2019/Data/MantidReducableData/Dec2020Data/'
    directBeamFile = 'DirectBeam_20feb_full_v3.dat'
    moderatorFile = 'ModeratorStdDev_TS2_SANS_LETexptl_07Aug2015.txt'
    lokiReduction = LokiSANSTestReduction(49338, 49339, 49334, 49335, 49335, dataFolder, directBeamFile, moderatorFile)
    lokiReduction.execute()
