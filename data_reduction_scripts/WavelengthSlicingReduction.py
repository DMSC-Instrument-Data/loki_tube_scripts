from mantid.simpleapi import *
from shutil import copy as shcopy
from fileinput import input as finp
from math import *
# import nxs as nxs
import os
from ISISCommandInterface import *
from mantid.api import WorkspaceGroup
from mantid.api import IEventWorkspace


# script to test SANS reduction using Q1D
# BEWARE the exaqmple currently here is for Dec2019 Loki detector tests which requires bespoke Larmor_Definition.xml and Larmor_Parameters.xml
# the precise logic of how an idf file is found is hazy, though we may be cheating by not giving a proper date range for validity of the tempoary idf.
# "Show instrument" will help diagnose issues, it may pick up Larmor_SEMSANS which is the last alphabetically.
# We could switch to a "normal" Larmor file instead.
#
# Note RKH more often uses WavRangeReduction rather than Q1D directly, as that pulls in much more from the user file by following the same route
# that the gui does and hides many of the lower level calls here.
# BEWARE if you do you that route then the encoder value for the Larmor detector banch angle is automatically applied, so for the Dec 2019 test we have to
# rotate it back ~89.8 degrees as the detector was not standing on the bench, see SET CENTRE in the user file.
#
# this version includes direct beam efficiency and transmission calculation, so the resulting I(Q) looks a lot more sensible, and the wavelength slice I(Q) are heading towards some sort of overlap.
#
# the full reduction also loads, reduces & then & subtracts the "can" run
# TODO: for both Q1d and WavRangeReduction it may be faster to do all the wavelength slices for sample, then for can, then the subtractions
# rather than slice for sample, slice for can, subtract.
#
def reduce(runnumber, transrun, transmt, wlist, idf_file, mask_file, db_file, filepath):
    wavesteps = str(wlist[0]) + ',-0.025,' + str(wlist[-1])
    ins = 'LARMOR000'
    nx = '.nxs'
    # load sample run, would save time debugging if check this exists or not
    LoadNexus(Filename=filepath + ins + str(runnumber) + nx, OutputWorkspace=ins + str(runnumber))

    # extract sans monitor in tof, then convert to wavelength
    ExtractSingleSpectrum(InputWorkspace=ins + str(runnumber), OutputWorkspace='sample_monitor', WorkspaceIndex=0)
    CalculateFlatBackground(InputWorkspace='sample_monitor', OutputWorkspace='sample_monitor', StartX=40000, EndX=99000,
                            Mode='Mean')
    ConvertUnits(InputWorkspace='sample_monitor', OutputWorkspace='sample_monitor', Target='Wavelength',
                 ConvertFromPointData=False)
    Rebin(InputWorkspace='sample_monitor', OutputWorkspace='sample_monitor', Params=wavesteps, PreserveEvents=False)
    # this removes one set of [ ] and converts array to list
    wav_values = mtd['sample_monitor'].extractX()[0].tolist()
    print('no of wav bins =', len(wav_values) - 1, 'wav_values =', wav_values)

    # convert sample run to wavelength
    ConvertUnits(InputWorkspace=ins + str(runnumber), OutputWorkspace='wavelength', Target='Wavelength',
                 ConvertFromPointData=False)
    # originally  Params='100' only gives one bin !
    Rebin(InputWorkspace='wavelength', OutputWorkspace='rebinned', Params=wavesteps, PreserveEvents=False)

    # load transmisssion runs, then subtract high end flat backgrounds in tof from monitors (not totally necessary, but easy enough to do), then convert to wavelength
    transfile = ins + str(transrun)
    transfile2 = transfile + '_mons'
    transfile3 = transfile + '_mons'
    LoadNexus(Filename=filepath + transfile + nx, OutputWorkspace=transfile)
    ExtractSpectra(InputWorkspace=transfile, OutputWorkspace=transfile2, DetectorList='1,4')
    CalculateFlatBackground(InputWorkspace=transfile2, OutputWorkspace=transfile2, StartX=40000, EndX=99000,
                            WorkspaceIndexList='0', Mode='Mean')
    CalculateFlatBackground(InputWorkspace=transfile2, OutputWorkspace=transfile2, StartX=88000, EndX=98000,
                            WorkspaceIndexList='1', Mode='Mean')
    ConvertUnits(InputWorkspace=transfile2, OutputWorkspace=transfile2, Target='Wavelength')
    Rebin(InputWorkspace=transfile2, OutputWorkspace=transfile2, Params=wavesteps)
    #
    transfile = ins + str(transmt)
    transfile2 = transfile + '_mons'
    LoadNexus(Filename=filepath + transfile + nx, OutputWorkspace=transfile)
    ExtractSpectra(InputWorkspace=transfile, OutputWorkspace=transfile2, DetectorList='1,4')
    CalculateFlatBackground(InputWorkspace=transfile2, OutputWorkspace=transfile2, StartX=40000, EndX=99000,
                            WorkspaceIndexList='0', Mode='Mean')
    CalculateFlatBackground(InputWorkspace=transfile2, OutputWorkspace=transfile2, StartX=88000, EndX=98000,
                            WorkspaceIndexList='1', Mode='Mean')
    ConvertUnits(InputWorkspace=transfile2, OutputWorkspace=transfile2, Target='Wavelength')
    Rebin(InputWorkspace=transfile2, OutputWorkspace=transfile2, Params=wavesteps)

    # removed RebinParams='0.9,-0.025,13.5', as already there
    CalculateTransmission(SampleRunWorkspace=transfile3, DirectRunWorkspace=transfile2, OutputWorkspace='trans_sample',
                          IncidentBeamMonitor=1, TransmissionMonitor=4, FitMethod='Polynomial', PolynomialOrder=3,
                          OutputUnfittedData=True)

    # read the db file, start the denominator i
    LoadRKH(Filename=filepath + db_file, OutputWorkspace='db_effic')
    ConvertToHistogram(InputWorkspace='db_effic', OutputWorkspace='norm')
    #
    RebinToWorkspace(WorkspaceToRebin='norm', WorkspaceToMatch='trans_sample', OutputWorkspace='norm')

    # multiply denom by incident SANS spectrum, & transmission,  should all already be in same wavelength bins 
    Multiply(LHSWorkspace='sample_monitor', RHSWorkspace='norm', OutputWorkspace='norm')
    Multiply(LHSWorkspace='trans_sample', RHSWorkspace='norm', OutputWorkspace='norm')

    # read the xml mask file
    LoadMask(idf_file, filepath + mask_file, RefWorkspace='rebinned', OutputWorkspace='loadedmask')
    maskwksp, maskdetlist = ExtractMask(InputWorkspace='loadedmask')
    print('maskdetlist=', maskdetlist)
    # MaskInstrument(InputWorkspace='rebinned', OutputWorkspace='rebinned_masked', DetectorIDs='maskdetlist')  # need convert array to list, decided to use MaskDetectors instead
    CloneWorkspace(InputWorkspace='rebinned', OutputWorkspace='rebinned_masked')
    MaskDetectors('rebinned_masked', MaskedWorkspace='maskwksp')

    ExtractSpectra(InputWorkspace='rebinned_masked', OutputWorkspace='extractall', StartWorkspaceIndex=13,
                   EndWorkspaceIndex=114697)

    # ought also to test:
    #    PixelAdj                - currently used for optional "flood source"  data, see MON/FLAT in user file
    #    WavePixelAdj        - currently used for optional correction to transmiissions for longer pathlength through sample at higher angles, see SAMPLE/PATH/ON in user file, and  online docs for SANSWideAngleCorrection
    #    RadiusCut and WaveCut  - option to gradually remove poor Q resolution data close to beam stop. See online docs for Q1D, this could be a WavePixelAdj but is, perhaps more efficiently, actually hard coded into Q1D.
    # CHECK that the beam centre is correct!
    Q1D(DetBankWorkspace='extractall', OutputWorkspace='Q1D_all', OutputBinning='0.005,-0.08,0.5', WavelengthAdj='norm',
        SolidAngleWeighting=True, AccountForGravity=True, ExtraLength=2, OutputParts=True)

    # now try some wavelength slices, keeping to exactly the same bin boundaries
    # (there may be some tiny rounding errors when using log bins due to the precision needed)
    wav_values_split, wav_index_split = split_wlist(wlist, wav_values)
    print('wav_values_split =', wav_values_split)
    print('wav_index_split =', wav_index_split)
    num_slices = len(wav_values_split) - 1
    w2 = wav_values_split[0]
    for i in range(0, num_slices):
        w1 = w2
        w2 = wav_values_split[i + 1]
        wavesteps = str(w1) + ',-0.025,' + str(w2)
        label = str(i + 1) + '_' + str(w1) + '_' + str(w2)
        print('slice =', i + 1, '  wav_index =', wav_index_split[i], ' to ', wav_index_split[i + 1], '  wavesteps =',
              wavesteps)

        # Rebin works, CropWorkspace should be faster still, but does not work, oops it only crops spectra, not X values with index va;ues
        #        Rebin(InputWorkspace='sample_monitor', OutputWorkspace='sample_monitor_slice', Params=wavesteps)
        #        Rebin(InputWorkspace='extractall', OutputWorkspace='extractall_slice', Params=wavesteps)
        #        Rebin(InputWorkspace='norm', OutputWorkspace='norm_slice', Params=wavesteps)

        #        CropWorkspace(InputWorkspace='sample_monitor', OutputWorkspace='sample_monitor_slice', StartWorkspaceIndex=wav_index_split[i], EndWorkspaceIndex=wav_index_split[i+1])
        #        CropWorkspace(InputWorkspace='extractall', OutputWorkspace='extractall_slice',  StartWorkspaceIndex=wav_index_split[i], EndWorkspaceIndex=wav_index_split[i+1])
        #        CropWorkspace(InputWorkspace='norm', OutputWorkspace='norm_slice',  StartWorkspaceIndex=wav_index_split[i], EndWorkspaceIndex=wav_index_split[i+1])
        CropWorkspace(InputWorkspace='sample_monitor', OutputWorkspace='sample_monitor_slice', XMin=w1, XMax=w2)
        CropWorkspace(InputWorkspace='extractall', OutputWorkspace='extractall_slice', XMin=w1, XMax=w2)
        CropWorkspace(InputWorkspace='norm', OutputWorkspace='norm_slice', XMin=w1, XMax=w2)

        Q1D(DetBankWorkspace='extractall_slice', OutputWorkspace='Q1D_' + label, OutputBinning='0.005,-0.08,0.5',
            WavelengthAdj='norm_slice', SolidAngleWeighting=True, AccountForGravity=True, ExtraLength=2,
            OutputParts=True)


# with help from stackoverflow ... this one puts the longer groupings towards the end of the list, which is what we want, see test code below.
def split_list(list, n):
    split = []
    for i in reversed(range(1, n + 1)):
        split_point = len(list) // i
        split.append(list[:split_point])
        list = list[split_point:]
    return split


# RKH, find nearest bin boundaries to those in wlist, then check theyare at least one bin wide
# assume both wlist and wavbins values are increasing
def split_wlist(wlist, wavbins):
    split1 = []
    index1 = []
    k = len(wavbins)
    tol = 1.e-06
    for w in wlist:
        # this starts search at top end each time then goes downwards, to first one lower than w, it is not very efficient, but we have to allow for all silly posibilities.
        j = k - 1
        # print('w=',w)
        while (w < wavbins[j] + tol):
            j -= 1
            if (j == 0):
                break
        if (j < k - 1):
            # check to see if next one up is nearer
            if ((wavbins[j + 1] - w) < (w - wavbins[j])):
                j += 1
        split1.append(wavbins[j])
        index1.append(j)
    # now merge any slices that are too narrow, this can likely be done by overwriting the top end of index & split instead of creating new ones
    split = []
    split.append(split1[0])
    index = []
    index.append(index1[0])
    k = 0
    for j in range(1, len(index1)):
        if (index1[j] > index[k]):
            k += 1
            split.append(split1[j])
            index.append(index1[j])
    return split, index


# ================================================================================================================================================================
#
#
#    (runnumber, transrun, transmt, ,number of wavelength slices,  idf_file,                                       mask_file,                             dbfile,                                              filepath)

wlist = [1.0, 2.5, 4.0, 6.0, 9.0, 13.5]
reduce("49338", "49339", "49335", wlist, "LARMOR_Definition.xml", "Mask_full_Jude_27Apr2020.xml",
       "DirectBeam_23Apr2020_L3_v24.dat", "c:/mantidinstall_OLD/data/Loki_Dec2019/")

# TODO: validate this method against the WavRangeReduction route - are the results OK?
# TODO check that  (sum numerators)/(sum denominators) = I(Q) for full range
'''
# test the splitter routines

wave=np.arange(0.9,13.5,0.2)

wlist=[.8,2.5,2.6,2.8,4.0,6.0,9.0,17.]
wlist=[.9,2.5,2.6,2.8,4.0,6.0,9.0,13.5]
split,index=split_wlist(wlist,wave)
print(wave)
print(wlist)
print(split)
print(index)


wave=np.arange(11)
print(wave)
for k in range(1,12):
    wave2=split_list(wave,k)
    print('k =',k,'   ',wave2)
    print(wave2[0][0])
    for j in range(0,k):
       print(wave2[j][-1])
'''
