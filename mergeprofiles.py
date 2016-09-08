#
# functions to read and load profiles

import os

import pandas as pd

import iofunctions as iof


def mergeProfiles(path, smoothingWindowUM, normalized = False, standardized=False):
    #return the merged profile for one image in a single document

    #list files for the readout
    csvFiles = iof.list_files(path, '.csv')
    txtFiles = iof.list_files(path, '.txt')

    #read metadata from csv
    profileMetaData = pd.read_csv(os.path.join(path,csvFiles[0]), sep=",")
    mergedProfiles = pd.DataFrame()
    imageName = profileMetaData.imageName[0]
    rostralPosition = profileMetaData.rostralPosition[0]
    normalizedSmoothening =[]
    standardizedSmoothening =[]

    #initialize from 1
    binNumber = 1
    for profileFileName in txtFiles:
        #read each profile
        AreaLabel = profileMetaData.Area[binNumber-1]
        Hemisphere = profileMetaData.Hemisphere[binNumber-1]

        #profile = readTrim(os.path.join(path,profileFileName),derivativeThreshold=derivativeThreshold, intensityThreshold=intensityThreshold, debugPrint=False)
        profile = iof.interpolateProfile(os.path.join(path, profileFileName),smoothingWindowUM, debugPrint=False)

        if standardized:
            standardizedSmoothening = (profile.smoothened - profile.smoothened.mean()) / (profile.smoothened.max() - profile.smoothened.min())
            profile.insert(4, "standardized", standardizedSmoothening)

        if normalized:
            normalizedSmoothening = profile.smoothened / profile.smoothened.max()
            profile.insert(4, "normalized", normalizedSmoothening)

        #normalize to mergw

        profile.insert(5, "Hemisphere", Hemisphere)
        profile.insert(6, "AreaLabel", AreaLabel)
        #merge
        mergedProfiles = mergedProfiles.append(profile)

        binNumber = binNumber+1

    mergedProfiles.insert(7, "rostralPosition", rostralPosition)
    mergedProfiles.insert(8, "genotype", iof.genotyping(imageName))

    #write merged profile to xlsx file
    mergedProfiles.to_excel(os.path.join(path,'mergedProfiles_'+imageName+'.xlsx'), sheet_name='Sheet1')

    return mergedProfiles