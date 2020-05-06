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

    maskingDetectorIDs = \
        """
        71961-71972,72473-72484,72985-72996,73497-73508,74009-74020,74521-74532,
        75033-75044,75545-75556,76057-76068,76569-76580,77081-77092,77593-77604,
        78105-78116,78617-78628,79129-79140,79641-79652,80153-80164,80665-80676,
        82201-82212,82713-82724,83225-83236,83737-83748,91929-91940,92441-92452,
        92953-92964,93465-93476,94489-94500,95001-95012,95513-95524,96025-96036,
        96537-96548,97049-97060,97561-97572,98073-98084,98585-98596,99097-99108,
        99609-99620,100121-100132,12-152,405-664,917-1176,1429-1688,1941-2200,
        2453-2712,2965-3224,3477-3736,3989-4248,4501-4760,5013-5272,5525-5784,
        6037-6296,6549-6808,7061-7320,7573-7832,8085-8344,8597-8856,9109-9368,
        9621-9880,10133-10392,10645-10904,11157-11416,11669-11928,12181-12440,
        12693-12952,13205-13464,13717-13976,14229-14488,14741-15000,15253-15512,
        15765-16024,16277-16536,16789-17048,17301-17560,17813-18072,18325-18584,
        18837-19096,19349-19608,19861-20120,20373-20632,20885-21144,21397-21656,
        21909-22168,22421-22680,22933-23192,23445-23704,23957-24216,24469-24728,
        24981-25240,25493-25752,26005-26264,26517-26776,27029-27288,27541-27800,
        28053-28312,28565-28824,29077-29336,29589-29848,30101-30360,30613-30872,
        31125-31384,31637-31896,32149-32408,32661-32920,33173-33432,33685-33944,
        34197-34456,34709-34968,35221-35480,35733-35992,36245-36504,36757-37016,
        37269-37528,37781-38040,38293-38552,38805-39064,39317-39576,39829-40088,
        40341-40600,40853-41112,41365-41624,41877-42136,42389-42648,42901-43160,
        43413-43672,43925-44184,44437-44696,44949-45208,45461-45720,45973-46232,
        46485-46744,46997-47256,47509-47768,48021-48280,48533-48792,49045-49304,
        49557-49816,50069-50328,50581-50840,51093-51352,51605-51864,52117-52376,
        52629-52888,53141-53400,53653-53912,54165-54424,54677-54936,55189-55448,
        55701-55960,56213-56472,56725-56984,57237-57467,57608-57631,57784-57979,
        58120-58143,58296-58491,58632-58655,58808-59003,59144-59167,59320-59515,
        59832-60027,60344-60539,60856-61051,61368-61563,61704-61727,61880-62075,
        62392-62587,62904-63099,63416-63611,63928-64123,64440-64635,64952-65147,
        65464-65659,65976-66171,66488-66683,67000-67195,67512-67707,68024-68219,
        68536-68731,69048-69243,69560-69755,70072-70267,70584-70779,71096-71291,
        71608-71803,71944-71967,72120-72315,72456-72479,72632-72827,72968-72991,
        73144-73339,73480-73503,73656-73851,73992-74015,74168-74363,74504-74527,
        74680-74875,75016-75039,75192-75387,75528-75551,75704-75899,76040-76063,
        76216-76411,76552-76575,76728-76923,77064-77087,77240-77435,77576-77599,
        77752-77947,78088-78111,78264-78459,78600-78623,78776-78971,79112-79135,
        79288-79483,79624-79647,79800-79995,80136-80159,80312-80507,80648-80671,
        80824-81019,81160-81183,81336-81531,81672-81695,81848-82043,82184-82207,
        82360-82555,82696-82719,82872-83067,83208-83231,83384-83579,83720-83743,
        83896-84091,84232-84255,84408-84603,84744-84767,84920-85115,85256-85279,
        85432-85627,85768-85791,85944-86139,86456-86651,86968-87163,87480-87675,
        87992-88187,88504-88699,88840-88863,89016-89211,89528-89723,90040-90235,
        90552-90747,91064-91259,91400-91423,91576-91771,91912-91935,92088-92283,
        92424-92447,92600-92795,92936-92959,93112-93307,93448-93471,93624-93819,
        94136-94331,94472-94495,94648-94843,94984-95007,95160-95355,95496-95519,
        95672-95867,96008-96031,96184-96379,96520-96543,96696-96891,97032-97055,
        97208-97403,97544-97567,97720-97915,98056-98079,98232-98427,98568-98591,
        98744-98939,99080-99103,99256-99451,99592-99615,99768-99963,100104-100127,
        100280-100475,100792-100987,101304-101499,101816-102011,102328-102523,
        102840-103035,103352-103547,103864-104059,104376-104571,104888-105083,
        105400-105595,105912-106107,106424-106619,106936-107131,107448-107643,
        107960-108155,108472-108667,108984-109179,109496-109691,110008-110203,
        110520-110715,111032-111227,111544-111739,112056-112251,112568-112763,
        113080-113275,113592-113787,114104-114299,114616-114698
        """

    def __init__(self, sampleRunNumber, sampleTransmissionRunNumber, backgroundRunNumber,
                 backgroundtransmissionRunNumber, dataFolderPath, directBeamFile, moderatorFile):
        self.sampleRun = sampleRunNumber
        self.sampleTransRun = sampleTransmissionRunNumber
        self.backgroundRun = backgroundRunNumber
        self.backgroundTransRun = backgroundtransmissionRunNumber
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
        self.sampleWsName = self._load(self.sampleRun, '_sans_nxs')
        return self.sampleWsName

    def _loadSampleTransmissionRun(self):
        self.sampleTransWsName = self._load(self.sampleTransRun, '_trans_nxs')
        return self.sampleTransWsName

    def _loadBackgroundRun(self):
        self.bgWsName = self._load(self.backgroundRun, '_sans_nxs')
        return self.bgWsName

    def _loadBackgroundTransmissionRun(self):
        self.bgTransWsName = self._load(self.backgroundTransRun, '_trans_nxs')
        return self.bgTransWsName

    def _loadAllData(self):
        samplePosZ = 0.30530
        benchPosY = 0.001
        self._moveSampleHolderAndDetectorBench(self._loadSampleRun(), samplePosZ, benchPosY)
        self._moveSampleHolderAndDetectorBench(self._loadBackgroundRun(), samplePosZ, benchPosY)
        self._moveSampleHolderAndDetectorBench(self._loadSampleTransmissionRun(), samplePosZ, benchPosY)
        self._moveSampleHolderAndDetectorBench(self._loadBackgroundTransmissionRun(), samplePosZ, benchPosY)

    def _applyMask(self, maskWs):
        maskWs = MaskBins(InputWorkspace=maskWs, InputWorkspaceIndexType='WorkspaceIndex', XMin=5, XMax=1500)
        maskWs = MaskBins(InputWorkspace=maskWs, InputWorkspaceIndexType='WorkspaceIndex', XMin=17500, XMax=19000)
        maskWs = MaskInstrument(InputWorkspace=maskWs, DetectorIDs=self.maskingDetectorIDs)
        # each detector mask must be applied separately
        MaskDetectorsInShape(Workspace=maskWs, ShapeXML=self.maskingCylinderXML)
        MaskDetectorsInShape(Workspace=maskWs, ShapeXML=self.maskingPlaneXML)
        return maskWs

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
        CalculateTransmission(SampleRunWorkspace=transWsTmp,
                              DirectRunWorkspace=transWsTmp,
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
    lokiReduction = LokiSANSTestReduction(49338, 49339, 49334, 49335, dataFolder, directBeamFile, moderatorFile)
    lokiReduction.execute()
