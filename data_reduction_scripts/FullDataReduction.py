
from mantid.simpleapi import *

import numpy
import csv

#def loadLOKIData(SAMPLE_SANS,BG_SANS,SAMPLE_TRANS,BG_TRANS,DB): 
def loadLOKIData(SampleSANS,SampleTRANS): 

    Load(Filename='/Users/judithhouston/Documents/ESS/LoKi/Design_documents/Detector/LarmorDec2019/Data/MantidReducableData/Dec2020Data/LARMOR000'+str(SampleSANS)+'.nxs', OutputWorkspace=str(SampleSANS)+'_sans_nxs')
    MoveInstrumentComponent(Workspace=str(SampleSANS)+'_sans_nxs', ComponentName='some-sample-holder', Z=0.30530000000000002)
    MoveInstrumentComponent(Workspace=str(SampleSANS)+'_sans_nxs', ComponentName='DetectorBench', Y=0.001)
#RotateInstrumentComponent(Workspace='49338_sans_nxs', ComponentName='DetectorBench', Y=1, Angle=89.498397827148438)

    Load(Filename='/Users/judithhouston/Documents/ESS/LoKi/Design_documents/Detector/LarmorDec2019/Data/MantidReducableData/Dec2020Data/LARMOR00049334.nxs', OutputWorkspace='49344_sans_nxs')
    MoveInstrumentComponent(Workspace='49344_sans_nxs', ComponentName='some-sample-holder', Z=0.30530000000000002)
    MoveInstrumentComponent(Workspace='49344_sans_nxs', ComponentName='DetectorBench', Y=0.001)
#RotateInstrumentComponent(Workspace='49344_sans_nxs', ComponentName='DetectorBench', Y=1, Angle=89.498397827148438)

    Load(Filename='/Users/judithhouston/Documents/ESS/LoKi/Design_documents/Detector/LarmorDec2019/Data/MantidReducableData/Dec2020Data/LARMOR000'+str(SampleTRANS)+'.nxs', OutputWorkspace=str(SampleTRANS)+'_trans_nxs')
    MoveInstrumentComponent(Workspace=str(SampleTRANS)+'_trans_nxs', ComponentName='some-sample-holder', Z=0.30530000000000002)
    MoveInstrumentComponent(Workspace=str(SampleTRANS)+'_trans_nxs', ComponentName='DetectorBench', Y=0.001)
#RotateInstrumentComponent(Workspace='49339_trans_nxs', ComponentName='DetectorBench', Y=1, Angle=89.498077392578125)

    Load(Filename='/Users/judithhouston/Documents/ESS/LoKi/Design_documents/Detector/LarmorDec2019/Data/MantidReducableData/Dec2020Data/LARMOR00049335.nxs', OutputWorkspace='49335_trans_nxs')
    MoveInstrumentComponent(Workspace='49335_trans_nxs', ComponentName='some-sample-holder', Z=0.30530000000000002)
    MoveInstrumentComponent(Workspace='49335_trans_nxs', ComponentName='DetectorBench', Y=0.001)
#RotateInstrumentComponent(Workspace='49335_trans_nxs', ComponentName='DetectorBench', Y=1, Angle=89.498237609863281)


    CloneWorkspace(InputWorkspace=str(SampleSANS)+'_sans_nxs', OutputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5')
    MaskBins(InputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5', InputWorkspaceIndexType='WorkspaceIndex', OutputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5', XMin=5, XMax=1500)
    MaskBins(InputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5', InputWorkspaceIndexType='WorkspaceIndex', OutputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5', XMin=17500, XMax=19000)
    
    #masking to check 
    MaskInstrument(InputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5', OutputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5', DetectorIDs='71961-71972,72473-72484,72985-72996,73497-73508,74009-74020,74521-74532,75033-75044,75545-75556,76057-76068,76569-76580,77081-77092,77593-77604,78105-78116,78617-78628,79129-79140,79641-79652,80153-80164,80665-80676,82201-82212,82713-82724,83225-83236,83737-83748,91929-91940,92441-92452,92953-92964,93465-93476,94489-94500,95001-95012,95513-95524,96025-96036,96537-96548,97049-97060,97561-97572,98073-98084,98585-98596,99097-99108,99609-99620,100121-100132,12-152,405-664,917-1176,1429-1688,1941-2200,2453-2712,2965-3224,3477-3736,3989-4248,4501-4760,5013-5272,5525-5784,6037-6296,6549-6808,7061-7320,7573-7832,8085-8344,8597-8856,9109-9368,9621-9880,10133-10392,10645-10904,11157-11416,11669-11928,12181-12440,12693-12952,13205-13464,13717-13976,14229-14488,14741-15000,15253-15512,15765-16024,16277-16536,16789-17048,17301-17560,17813-18072,18325-18584,18837-19096,19349-19608,19861-20120,20373-20632,20885-21144,21397-21656,21909-22168,22421-22680,22933-23192,23445-23704,23957-24216,24469-24728,24981-25240,25493-25752,26005-26264,26517-26776,27029-27288,27541-27800,28053-28312,28565-28824,29077-29336,29589-29848,30101-30360,30613-30872,31125-31384,31637-31896,32149-32408,32661-32920,33173-33432,33685-33944,34197-34456,34709-34968,35221-35480,35733-35992,36245-36504,36757-37016,37269-37528,37781-38040,38293-38552,38805-39064,39317-39576,39829-40088,40341-40600,40853-41112,41365-41624,41877-42136,42389-42648,42901-43160,43413-43672,43925-44184,44437-44696,44949-45208,45461-45720,45973-46232,46485-46744,46997-47256,47509-47768,48021-48280,48533-48792,49045-49304,49557-49816,50069-50328,50581-50840,51093-51352,51605-51864,52117-52376,52629-52888,53141-53400,53653-53912,54165-54424,54677-54936,55189-55448,55701-55960,56213-56472,56725-56984,57237-57467,57608-57631,57784-57979,58120-58143,58296-58491,58632-58655,58808-59003,59144-59167,59320-59515,59832-60027,60344-60539,60856-61051,61368-61563,61704-61727,61880-62075,62392-62587,62904-63099,63416-63611,63928-64123,64440-64635,64952-65147,65464-65659,65976-66171,66488-66683,67000-67195,67512-67707,68024-68219,68536-68731,69048-69243,69560-69755,70072-70267,70584-70779,71096-71291,71608-71803,71944-71967,72120-72315,72456-72479,72632-72827,72968-72991,73144-73339,73480-73503,73656-73851,73992-74015,74168-74363,74504-74527,74680-74875,75016-75039,75192-75387,75528-75551,75704-75899,76040-76063,76216-76411,76552-76575,76728-76923,77064-77087,77240-77435,77576-77599,77752-77947,78088-78111,78264-78459,78600-78623,78776-78971,79112-79135,79288-79483,79624-79647,79800-79995,80136-80159,80312-80507,80648-80671,80824-81019,81160-81183,81336-81531,81672-81695,81848-82043,82184-82207,82360-82555,82696-82719,82872-83067,83208-83231,83384-83579,83720-83743,83896-84091,84232-84255,84408-84603,84744-84767,84920-85115,85256-85279,85432-85627,85768-85791,85944-86139,86456-86651,86968-87163,87480-87675,87992-88187,88504-88699,88840-88863,89016-89211,89528-89723,90040-90235,90552-90747,91064-91259,91400-91423,91576-91771,91912-91935,92088-92283,92424-92447,92600-92795,92936-92959,93112-93307,93448-93471,93624-93819,94136-94331,94472-94495,94648-94843,94984-95007,95160-95355,95496-95519,95672-95867,96008-96031,96184-96379,96520-96543,96696-96891,97032-97055,97208-97403,97544-97567,97720-97915,98056-98079,98232-98427,98568-98591,98744-98939,99080-99103,99256-99451,99592-99615,99768-99963,100104-100127,100280-100475,100792-100987,101304-101499,101816-102011,102328-102523,102840-103035,103352-103547,103864-104059,104376-104571,104888-105083,105400-105595,105912-106107,106424-106619,106936-107131,107448-107643,107960-108155,108472-108667,108984-109179,109496-109691,110008-110203,110520-110715,111032-111227,111544-111739,112056-112251,112568-112763,113080-113275,113592-113787,114104-114299,114616-114698')

    MaskDetectorsInShape(Workspace=str(SampleSANS)+'rear_1D_0.9_13.5', ShapeXML='<infinite-cylinder id="beam_stop"><centre x="0" y="0" z="0.0" /><axis x="0" y="0" z="1" /><radius val="0.045" /></infinite-cylinder><algebra val="beam_stop"/>')
    MaskDetectorsInShape(Workspace=str(SampleSANS)+'rear_1D_0.9_13.5', ShapeXML='<infinite-plane id="unique phi_plane1"><point-in-plane x="0" y="0" z="0" /><normal-to-plane x="-1.0" y="-1.22464679915e-16" z="0" /></infinite-plane><infinite-plane id="unique phi_plane2"><point-in-plane x="0" y="0" z="0" /><normal-to-plane x="-1.0" y="-2.44929359829e-16" z="0" /></infinite-plane><infinite-plane id="unique phi_plane3"><point-in-plane x="0" y="0" z="0" /><normal-to-plane x="1.0" y="2.44929359829e-16" z="0" /></infinite-plane><infinite-plane id="unique phi_plane4"><point-in-plane x="0" y="0" z="0" /><normal-to-plane x="1.0" y="1.22464679915e-16" z="0" /></infinite-plane><algebra val="#((unique phi_plane1 unique phi_plane2):(unique phi_plane3 unique phi_plane4))" />')
    ConvertUnits(InputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5', OutputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5', Target='Wavelength')
    Rebin(InputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5', OutputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5', Params='0.9,-0.025,13.5')
    ExtractSingleSpectrum(InputWorkspace=str(SampleSANS)+'_sans_nxs', OutputWorkspace='_Sample__monitor', WorkspaceIndex=0)
    RenameWorkspace(InputWorkspace='_Sample__monitor', OutputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5_incident_monitor')
    CalculateFlatBackground(InputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5_incident_monitor', OutputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5_incident_monitor', StartX=40000, EndX=99000, Mode='Mean')
    ConvertUnits(InputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5_incident_monitor', OutputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5_incident_monitor', Target='Wavelength')
    Rebin(InputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5_incident_monitor', OutputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5_incident_monitor', Params='0.9,-0.025,13.5')
    
    
    ExtractSpectra(InputWorkspace=str(SampleTRANS)+'_trans_nxs', OutputWorkspace=str(SampleTRANS)+'_trans_nxs_tmp', DetectorList='1,4')
    CalculateFlatBackground(InputWorkspace=str(SampleTRANS)+'_trans_nxs_tmp', OutputWorkspace=str(SampleTRANS)+'_trans_nxs_tmp', StartX=40000, EndX=99000, WorkspaceIndexList='0', Mode='Mean')
    CalculateFlatBackground(InputWorkspace=str(SampleTRANS)+'_trans_nxs_tmp', OutputWorkspace=str(SampleTRANS)+'_trans_nxs_tmp', StartX=88000, EndX=98000, WorkspaceIndexList='1', Mode='Mean')
    ConvertUnits(InputWorkspace=str(SampleTRANS)+'_trans_nxs_tmp', OutputWorkspace=str(SampleTRANS)+'_trans_nxs_tmp', Target='Wavelength')
    Rebin(InputWorkspace=str(SampleTRANS)+'_trans_nxs_tmp', OutputWorkspace=str(SampleTRANS)+'_trans_nxs_tmp', Params='0.9,-0.025,13.5')
    
    
    ExtractSpectra(InputWorkspace='49335_trans_nxs', OutputWorkspace='49335_trans_nxs_tmp', DetectorList='1,4')
    CalculateFlatBackground(InputWorkspace='49335_trans_nxs_tmp', OutputWorkspace='49335_trans_nxs_tmp', StartX=40000, EndX=99000, WorkspaceIndexList='0', Mode='Mean')
    CalculateFlatBackground(InputWorkspace='49335_trans_nxs_tmp', OutputWorkspace='49335_trans_nxs_tmp', StartX=88000, EndX=98000, WorkspaceIndexList='1', Mode='Mean')
    ConvertUnits(InputWorkspace='49335_trans_nxs_tmp', OutputWorkspace='49335_trans_nxs_tmp', Target='Wavelength')
    Rebin(InputWorkspace='49335_trans_nxs_tmp', OutputWorkspace='49335_trans_nxs_tmp', Params='0.9,-0.025,13.5')
    
    CalculateTransmission(SampleRunWorkspace=str(SampleTRANS)+'_trans_nxs_tmp', DirectRunWorkspace='49335_trans_nxs_tmp', OutputWorkspace=str(SampleTRANS)+'_trans_sample_0.9_13.5', IncidentBeamMonitor=1, TransmissionMonitor=4, RebinParams='0.9,-0.025,13.5', FitMethod='Polynomial', PolynomialOrder=3, OutputUnfittedData=True)
    CreateSingleValuedWorkspace(OutputWorkspace='__python_binary_op_single_value', DataValue=100)
    Multiply(LHSWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5', RHSWorkspace='__python_binary_op_single_value', OutputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5')
    CreateSingleValuedWorkspace(OutputWorkspace='__python_binary_op_single_value', DataValue=176.71458676442586)
    Divide(LHSWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5', RHSWorkspace='__python_binary_op_single_value', OutputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5')
    LoadRKH(Filename='/Users/judithhouston/Documents/ESS/LoKi/Design_documents/Detector/LarmorDec2019/Data/MantidReducableData/DirectBeam_20feb_full_v3.dat', OutputWorkspace='__CalculateNormISIS_loaded_tmp')
    ConvertToHistogram(InputWorkspace='__CalculateNormISIS_loaded_tmp', OutputWorkspace='__CalculateNormISIS_loaded_tmp')
    RebinToWorkspace(WorkspaceToRebin='__CalculateNormISIS_loaded_tmp', WorkspaceToMatch=str(SampleSANS)+'rear_1D_0.9_13.5', OutputWorkspace='__CalculateNorm_loaded_temp')
    RenameWorkspace(InputWorkspace='__CalculateNorm_loaded_temp', OutputWorkspace='__Q_WAVE_conversion_temp')
    RebinToWorkspace(WorkspaceToRebin=str(SampleSANS)+'rear_1D_0.9_13.5_incident_monitor', WorkspaceToMatch=str(SampleSANS)+'rear_1D_0.9_13.5', OutputWorkspace='__CalculateNorm_loaded_temp')
    Multiply(LHSWorkspace='__CalculateNorm_loaded_temp', RHSWorkspace='__Q_WAVE_conversion_temp', OutputWorkspace='__Q_WAVE_conversion_temp')
    RebinToWorkspace(WorkspaceToRebin=str(SampleTRANS)+'_trans_sample_0.9_13.5', WorkspaceToMatch=str(SampleSANS)+'rear_1D_0.9_13.5', OutputWorkspace='__CalculateNorm_loaded_temp')
    Multiply(LHSWorkspace='__CalculateNorm_loaded_temp', RHSWorkspace='__Q_WAVE_conversion_temp', OutputWorkspace='__Q_WAVE_conversion_temp')
    LoadRKH(Filename='/Users/judithhouston/Documents/ESS/LoKi/Design_documents/Detector/LarmorTestsJune2019/LoKIReductionFiles/ModeratorStdDev_TS2_SANS_LETexptl_07Aug2015.txt', OutputWorkspace='moderator_ws')
    ConvertToHistogram(InputWorkspace='moderator_ws', OutputWorkspace='moderator_histogram_ws')
    TOFSANSResolutionByPixel(InputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5', OutputWorkspace='Q_Resolution_ISIS_SANS', DeltaR=8, SampleApertureRadius=4.0824829046386295, SourceApertureRadius=14.433756729740645, SigmaModerator='moderator_histogram_ws', CollimationLength=5, AccountForGravity=True, ExtraLength=2)
    Q1D(DetBankWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5', OutputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5', OutputBinning='0.0045,-0.08,0.7', WavelengthAdj='__Q_WAVE_conversion_temp', AccountForGravity=True, ExtraLength=2, QResolution='Q_Resolution_ISIS_SANS')
    RenameWorkspace(InputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5', OutputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5_sam_tmp')
    CloneWorkspace(InputWorkspace='49344_sans_nxs', OutputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5_can_tmp')
    MaskBins(InputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5_can_tmp', InputWorkspaceIndexType='WorkspaceIndex', OutputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5_can_tmp', XMin=5, XMax=1500)
    MaskBins(InputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5_can_tmp', InputWorkspaceIndexType='WorkspaceIndex', OutputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5_can_tmp', XMin=17500, XMax=19000)
    
    MaskInstrument(InputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5_can_tmp', OutputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5_can_tmp', DetectorIDs='71961-71972,72473-72484,72985-72996,73497-73508,74009-74020,74521-74532,75033-75044,75545-75556,76057-76068,76569-76580,77081-77092,77593-77604,78105-78116,78617-78628,79129-79140,79641-79652,80153-80164,80665-80676,82201-82212,82713-82724,83225-83236,83737-83748,91929-91940,92441-92452,92953-92964,93465-93476,94489-94500,95001-95012,95513-95524,96025-96036,96537-96548,97049-97060,97561-97572,98073-98084,98585-98596,99097-99108,99609-99620,100121-100132,12-152,405-664,917-1176,1429-1688,1941-2200,2453-2712,2965-3224,3477-3736,3989-4248,4501-4760,5013-5272,5525-5784,6037-6296,6549-6808,7061-7320,7573-7832,8085-8344,8597-8856,9109-9368,9621-9880,10133-10392,10645-10904,11157-11416,11669-11928,12181-12440,12693-12952,13205-13464,13717-13976,14229-14488,14741-15000,15253-15512,15765-16024,16277-16536,16789-17048,17301-17560,17813-18072,18325-18584,18837-19096,19349-19608,19861-20120,20373-20632,20885-21144,21397-21656,21909-22168,22421-22680,22933-23192,23445-23704,23957-24216,24469-24728,24981-25240,25493-25752,26005-26264,26517-26776,27029-27288,27541-27800,28053-28312,28565-28824,29077-29336,29589-29848,30101-30360,30613-30872,31125-31384,31637-31896,32149-32408,32661-32920,33173-33432,33685-33944,34197-34456,34709-34968,35221-35480,35733-35992,36245-36504,36757-37016,37269-37528,37781-38040,38293-38552,38805-39064,39317-39576,39829-40088,40341-40600,40853-41112,41365-41624,41877-42136,42389-42648,42901-43160,43413-43672,43925-44184,44437-44696,44949-45208,45461-45720,45973-46232,46485-46744,46997-47256,47509-47768,48021-48280,48533-48792,49045-49304,49557-49816,50069-50328,50581-50840,51093-51352,51605-51864,52117-52376,52629-52888,53141-53400,53653-53912,54165-54424,54677-54936,55189-55448,55701-55960,56213-56472,56725-56984,57237-57467,57608-57631,57784-57979,58120-58143,58296-58491,58632-58655,58808-59003,59144-59167,59320-59515,59832-60027,60344-60539,60856-61051,61368-61563,61704-61727,61880-62075,62392-62587,62904-63099,63416-63611,63928-64123,64440-64635,64952-65147,65464-65659,65976-66171,66488-66683,67000-67195,67512-67707,68024-68219,68536-68731,69048-69243,69560-69755,70072-70267,70584-70779,71096-71291,71608-71803,71944-71967,72120-72315,72456-72479,72632-72827,72968-72991,73144-73339,73480-73503,73656-73851,73992-74015,74168-74363,74504-74527,74680-74875,75016-75039,75192-75387,75528-75551,75704-75899,76040-76063,76216-76411,76552-76575,76728-76923,77064-77087,77240-77435,77576-77599,77752-77947,78088-78111,78264-78459,78600-78623,78776-78971,79112-79135,79288-79483,79624-79647,79800-79995,80136-80159,80312-80507,80648-80671,80824-81019,81160-81183,81336-81531,81672-81695,81848-82043,82184-82207,82360-82555,82696-82719,82872-83067,83208-83231,83384-83579,83720-83743,83896-84091,84232-84255,84408-84603,84744-84767,84920-85115,85256-85279,85432-85627,85768-85791,85944-86139,86456-86651,86968-87163,87480-87675,87992-88187,88504-88699,88840-88863,89016-89211,89528-89723,90040-90235,90552-90747,91064-91259,91400-91423,91576-91771,91912-91935,92088-92283,92424-92447,92600-92795,92936-92959,93112-93307,93448-93471,93624-93819,94136-94331,94472-94495,94648-94843,94984-95007,95160-95355,95496-95519,95672-95867,96008-96031,96184-96379,96520-96543,96696-96891,97032-97055,97208-97403,97544-97567,97720-97915,98056-98079,98232-98427,98568-98591,98744-98939,99080-99103,99256-99451,99592-99615,99768-99963,100104-100127,100280-100475,100792-100987,101304-101499,101816-102011,102328-102523,102840-103035,103352-103547,103864-104059,104376-104571,104888-105083,105400-105595,105912-106107,106424-106619,106936-107131,107448-107643,107960-108155,108472-108667,108984-109179,109496-109691,110008-110203,110520-110715,111032-111227,111544-111739,112056-112251,112568-112763,113080-113275,113592-113787,114104-114299,114616-114698')

    MaskDetectorsInShape(Workspace=str(SampleSANS)+'rear_1D_0.9_13.5_can_tmp', ShapeXML='<infinite-cylinder id="beam_stop"><centre x="0" y="0" z="0.0" /><axis x="0" y="0" z="1" /><radius val="0.045" /></infinite-cylinder><algebra val="beam_stop"/>')
    MaskDetectorsInShape(Workspace=str(SampleSANS)+'rear_1D_0.9_13.5_can_tmp', ShapeXML='<infinite-plane id="unique phi_plane1"><point-in-plane x="0" y="0" z="0" /><normal-to-plane x="-1.0" y="-1.22464679915e-16" z="0" /></infinite-plane><infinite-plane id="unique phi_plane2"><point-in-plane x="0" y="0" z="0" /><normal-to-plane x="-1.0" y="-2.44929359829e-16" z="0" /></infinite-plane><infinite-plane id="unique phi_plane3"><point-in-plane x="0" y="0" z="0" /><normal-to-plane x="1.0" y="2.44929359829e-16" z="0" /></infinite-plane><infinite-plane id="unique phi_plane4"><point-in-plane x="0" y="0" z="0" /><normal-to-plane x="1.0" y="1.22464679915e-16" z="0" /></infinite-plane><algebra val="#((unique phi_plane1 unique phi_plane2):(unique phi_plane3 unique phi_plane4))" />')
    ConvertUnits(InputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5_can_tmp', OutputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5_can_tmp', Target='Wavelength')
    Rebin(InputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5_can_tmp', OutputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5_can_tmp', Params='0.9,-0.025,13.5')
    ExtractSingleSpectrum(InputWorkspace='49344_sans_nxs', OutputWorkspace='_Sample__monitor', WorkspaceIndex=0)
    RenameWorkspace(InputWorkspace='_Sample__monitor', OutputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5_can_tmp_incident_monitor')
    CalculateFlatBackground(InputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5_can_tmp_incident_monitor', OutputWorkspace='49338rear_1D_0.9_13.5_can_tmp_incident_monitor', StartX=40000, EndX=99000, Mode='Mean')
    ConvertUnits(InputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5_can_tmp_incident_monitor', OutputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5_can_tmp_incident_monitor', Target='Wavelength')
    Rebin(InputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5_can_tmp_incident_monitor', OutputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5_can_tmp_incident_monitor', Params='0.9,-0.025,13.5')
    ExtractSpectra(InputWorkspace='49335_trans_nxs', OutputWorkspace='49335_trans_nxs_tmp', DetectorList='1,4')
    CalculateFlatBackground(InputWorkspace='49335_trans_nxs_tmp', OutputWorkspace='49335_trans_nxs_tmp', StartX=40000, EndX=99000, WorkspaceIndexList='0', Mode='Mean')
    CalculateFlatBackground(InputWorkspace='49335_trans_nxs_tmp', OutputWorkspace='49335_trans_nxs_tmp', StartX=88000, EndX=98000, WorkspaceIndexList='1', Mode='Mean')
    ConvertUnits(InputWorkspace='49335_trans_nxs_tmp', OutputWorkspace='49335_trans_nxs_tmp', Target='Wavelength')
    Rebin(InputWorkspace='49335_trans_nxs_tmp', OutputWorkspace='49335_trans_nxs_tmp', Params='0.9,-0.025,13.5')
    CalculateTransmission(SampleRunWorkspace='49335_trans_nxs_tmp', DirectRunWorkspace='49335_trans_nxs_tmp', OutputWorkspace='49335_trans_can_0.9_13.5', IncidentBeamMonitor=1, TransmissionMonitor=4, RebinParams='0.9,-0.025,13.5', FitMethod='Polynomial', PolynomialOrder=3, OutputUnfittedData=True)
    CreateSingleValuedWorkspace(OutputWorkspace='__python_binary_op_single_value', DataValue=100)
    Multiply(LHSWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5_can_tmp', RHSWorkspace='__python_binary_op_single_value', OutputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5_can_tmp')
    CreateSingleValuedWorkspace(OutputWorkspace='__python_binary_op_single_value', DataValue=176.71458676442586)
    Divide(LHSWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5_can_tmp', RHSWorkspace='__python_binary_op_single_value', OutputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5_can_tmp')
    LoadRKH(Filename='/Users/judithhouston/Documents/ESS/LoKi/Design_documents/Detector/LarmorDec2019/Data/MantidReducableData/DirectBeam_20feb_full_v3.dat', OutputWorkspace='__CalculateNormISIS_loaded_tmp')
    ConvertToHistogram(InputWorkspace='__CalculateNormISIS_loaded_tmp', OutputWorkspace='__CalculateNormISIS_loaded_tmp')
    RebinToWorkspace(WorkspaceToRebin='__CalculateNormISIS_loaded_tmp', WorkspaceToMatch=str(SampleSANS)+'rear_1D_0.9_13.5_can_tmp', OutputWorkspace='__CalculateNorm_loaded_temp')
    RenameWorkspace(InputWorkspace='__CalculateNorm_loaded_temp', OutputWorkspace='__Q_WAVE_conversion_temp')
    RebinToWorkspace(WorkspaceToRebin=str(SampleSANS)+'rear_1D_0.9_13.5_can_tmp_incident_monitor', WorkspaceToMatch=str(SampleSANS)+'rear_1D_0.9_13.5_can_tmp', OutputWorkspace='__CalculateNorm_loaded_temp')
    Multiply(LHSWorkspace='__CalculateNorm_loaded_temp', RHSWorkspace='__Q_WAVE_conversion_temp', OutputWorkspace='__Q_WAVE_conversion_temp')
    RebinToWorkspace(WorkspaceToRebin='49335_trans_can_0.9_13.5', WorkspaceToMatch=str(SampleSANS)+'rear_1D_0.9_13.5_can_tmp', OutputWorkspace='__CalculateNorm_loaded_temp')
    Multiply(LHSWorkspace='__CalculateNorm_loaded_temp', RHSWorkspace='__Q_WAVE_conversion_temp', OutputWorkspace='__Q_WAVE_conversion_temp')
    LoadRKH(Filename='/Users/judithhouston/Documents/ESS/LoKi/Design_documents/Detector/LarmorTestsJune2019/LoKIReductionFiles/ModeratorStdDev_TS2_SANS_LETexptl_07Aug2015.txt', OutputWorkspace='moderator_ws')
    ConvertToHistogram(InputWorkspace='moderator_ws', OutputWorkspace='moderator_histogram_ws')
    TOFSANSResolutionByPixel(InputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5_can_tmp', OutputWorkspace='Q_Resolution_ISIS_SANS', DeltaR=8, SampleApertureRadius=4.0824829046386295, SourceApertureRadius=14.433756729740645, SigmaModerator='moderator_histogram_ws', CollimationLength=5, AccountForGravity=True, ExtraLength=2)
    Q1D(DetBankWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5_can_tmp', OutputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5_can_tmp', OutputBinning='0.0045,-0.08,0.7', WavelengthAdj='__Q_WAVE_conversion_temp', AccountForGravity=True, ExtraLength=2, QResolution='Q_Resolution_ISIS_SANS')
    Minus(LHSWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5_sam_tmp', RHSWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5_can_tmp', OutputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5')
    CropWorkspace(InputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5', OutputWorkspace=str(SampleSANS)+'rear_1D_0.9_13.5', XMin=0.008, XMax=0.6)
    AddSampleLog(Workspace=str(SampleSANS)+'rear_1D_0.9_13.5', LogName='UserFile', LogText='/Users/judithhouston/Documents/ESS/LoKi/Design_documents/Detector/LarmorDec2019/Data/MantidReducableData/USER_Raspino_191E_BCSLarmor_24Feb2020_v1.txt')
    AddSampleLog(Workspace=str(SampleSANS)+'rear_1D_0.9_13.5', LogName='Transmission', LogText=str(SampleTRANS)+'_trans_sample_0.9_13.5_unfitted')
    AddSampleLog(Workspace=str(SampleSANS)+'rear_1D_0.9_13.5', LogName='TransmissionCan', LogText='49335_trans_can_0.9_13.5_unfitted')


if __name__ == "__main__":
    loadLOKIData(49334,49335)