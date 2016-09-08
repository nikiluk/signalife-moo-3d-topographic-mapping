#
# functions to process file loading and data manipulation

import datetime
import os

import numpy as np
import pandas as pd
from scipy import interpolate

import smoothingfunctions as smoo


def list_files(path,ext):
    # returns a list of names (with extension, without full path) of all files
    # in folder path ext could be '.txt'
    #

    files = []
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)):
            if ext in name:
                files.append(name)
    return files

def printDate():
    # returns the string with the current date/time in minute
    # example output '2016-05-23_16-31'

    printDate =  datetime.datetime.now().isoformat().replace(":", "-")[:16].replace("T", "_")
    return printDate

def outputFile(fileName, projectFolder=os.getcwd(), folderSuffix='_output'):
    # creates the output folder with current datetime and returns the path url for the file to be used further
    outputFolder = os.path.join(projectFolder, printDate() + folderSuffix)
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)
    outputFile = os.path.join(outputFolder, fileName)
    return outputFile




def intensityThresholding(inputProfile, intensityColumn='intensity', intensityThreshold=0):
    #drop rows with intensity les than threshold

    inputProfile = inputProfile[inputProfile[intensityColumn] > intensityThreshold]
    outputProfile = inputProfile.reset_index(drop=True)

    return outputProfile





def readTrim(location, derivativeThreshold=2,intensityThreshold=0,debugPrint=False):
    #read profile files into pd.dataframe and trim empty beginning before the derivative
    #

    #read from txt
    input = pd.read_csv(location, index_col=0, sep="\t")

    #drop low intensity
    if debugPrint:
        print("Length raw: "+str(len(input)))

    #apply threshold on intensity
    input = intensityThresholding(input, "intensity" ,intensityThreshold=intensityThreshold)

    if debugPrint:
        print("Length intensity threshold cut: "+str(len(input)))

    # renaming columns for furter normalization + saving parameters


    voxelWidth = float(input.columns.values[1])
    input.columns.values[1] = "voxelWidth"
    binNumber = input.columns.values[2]
    input.columns.values[2] = "binNumber"
    imageName = input.columns.values[3]
    input.columns.values[3] = "imageName"

    if debugPrint:
        print(voxelWidth)

    #initialize distance
    input.insert(1, "distance", np.zeros(len(input)))

    smoothingWindowPX = smoo.smoothingWindowUM2PX(smoothingWindowUM, voxelWidth)
    smoothened = smoo.smoothFunc(input.intensity, smoothingWindowPX)
    if debugPrint:
        print("Length after smoothened: "+str(len(smoothened)))

    input.insert(2, "smoothened", smoothened)

    #apply threshold on smoothened intensity
    input = intensityThresholding(input, "smoothened" ,intensityThreshold=intensityThreshold)

    if debugPrint:
        print("Length smoothened cut: "+str(len(input)))

    #calculate smoothed derivative
    derivative = np.zeros(len(input))
    for m in input.index.values:
        if m == 0:
            derivative[m] = 0 # to prevent wrong cut-offs because of the steep increase in derivative
        else:
            derivative[m] = (input.smoothened[m] - input.smoothened[m - 1]) / voxelWidth
    input.insert(3, "derivative", derivative)

    #find the index of the first element in the dataframe matching condition
    # for m in input.index.values:
    #     if derivative[m-1] == nxt:
    #         dropIndex = m-1
    #         #print(dropIndex*voxelWidth)
    #         break
    #
    # print(nxt)
    # print()

    #using shorter version
    # nxt = next(x for x in input.derivative if x > derivativeThreshold)
    # dropIndex = int(input[input['derivative'] == nxt].index.values[0])
    #
    # profile = input[dropIndex:].reset_index(drop=True)
    #
    # #print(profile.head(20))
    # if debugPrint:
    #     print("Drop index: "+str(dropIndex))

    profile = input

    #populate the distance column
    distance = np.array(profile.index.values.tolist()) + 0.
    distance = distance * voxelWidth
    profile.distance = distance

    # normalizing data for future merge of the tables and metadata
    profile.binNumber = binNumber
    profile.imageName = imageName
    profile.voxelWidth = voxelWidth

    return profile



def genotyping(imageName):
    #depending on imageName returns the genotype string

    #genotype filtering
    list_WT = ['f-f_cre-neg','f-p_cre-neg','p-p_cre-neg','p-p_cre-pos']
    list_CKO = ['f-f_cre-pos']
    list_HTZ = ['f-p_cre-pos']


    if any(ext in str(imageName) for ext in list_CKO):
        return 'CKO'
    if any(ext in str(imageName) for ext in list_WT):
        return 'WT'
    if any(ext in str(imageName) for ext in list_HTZ):
        return 'HTZ'



def averageProfiles(allProfiles):
    #finding average of the profile by length within certain area

    return averagedProfiles





def plotPivotProfiles(pivotProfiles, imageName, titlePrefix="", showPlot=True):
    #plot the profiles from the dataframe, each profile is a plot for each dataframe column
    #save them to excel
    plt.figure()

    if not showPlot:
        plt.ioff()

    pivotProfiles.plot(subplots=False, figsize=(22, 11), linewidth=2.0, title=titlePrefix+imageName)
    plt.savefig(os.path.join(path,'img_all_'+titlePrefix+imageName+'.png'))

    if not showPlot:
        plt.close()

    pivotProfiles.plot(subplots=True, figsize=(11, 16), linewidth=2.0, title=titlePrefix+imageName)
    plt.savefig(os.path.join(path,'img_sub_'+titlePrefix+imageName+'.png'))
    plt.legend()

    if not showPlot:
        plt.close()

    pivotProfiles.to_excel(os.path.join(path ,'pivotProfiles_'+titlePrefix+imageName+'.xlsx'), sheet_name='Sheet1')



def interpolateProfile(location,smoothingWindowUM,debugPrint=False):
    #read profile files into pd.dataframe, smooth and interpolate them with 1um step (make the profile resolution-independent)
    #

    #read profile information from txt files produced by fiji macros
    input = pd.read_csv(location, index_col=0, sep="\t")

    if debugPrint:
        print("Length raw: "+str(len(input)))

    voxelWidth = float(input.columns.values[1])
    input.columns.values[1] = "voxelWidth"
    binNumber = input.columns.values[2]
    input.columns.values[2] = "binNumber"
    imageName = input.columns.values[3]
    input.columns.values[3] = "imageName"

    #initialize distance
    input.insert(1, "distance", np.zeros(len(input)))

    smoothingWindowPX = smoo.smoothingWindowUM2PX(smoothingWindowUM, voxelWidth)
    smoothened = smoo.smoothFunc(input.intensity, smoothingWindowPX)
    if debugPrint:
        print("Length after smoothened: "+str(len(smoothened)))

    input.insert(2, "smoothened", smoothened)

    #populate the distance column
    distance = np.array(input.index.values.tolist()) + 1.
    distance = distance * voxelWidth
    input.distance = distance

    yOld = input.smoothened
    xOld = input.distance
    lenNew = int(xOld.max())-1 #um length of the profile bin, int

    interpolateObj = interpolate.interp1d(xOld, yOld, kind='cubic', bounds_error=False)
    #xNew = np.arange(0, lenNew, 1)
    xNew = np.linspace(1, lenNew, lenNew)
    yNew = interpolateObj(xNew)

    profile = pd.DataFrame()
    profile.insert(0, "smoothened", yNew)
    profile.insert(1, "binNumber", binNumber)
    profile.insert(2, "imageName", imageName)
    profile.insert(3, "voxelWidth", voxelWidth)
    profile.insert(4, "distance", xNew)
    profile.index = xNew

    # normalizing data for future merge of the tables and metadata
    # profile.binNumber = binNumber
    # profile.imageName = imageName
    # profile.voxelWidth = voxelWidth

    return profile