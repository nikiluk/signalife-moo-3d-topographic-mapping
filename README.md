3D topographic mapping for biological images
============================================

This package is created to help biologists in distinguishing different tissue areas depending on fluorescence intensity. The general idea of the approach is somewhat similar to surface plot, where z-dimension is created from the pixel intensity, but with the crucial difference in a direction along which the intensity profiles are collected.

How it works
-------------

**First**, ImageJ macros calculates intensity profile of rectangular bins along the set of user-defined pairs of points. The intensity information is collected automatically along the longest side and averaged along the shortest side. Each intensity profile is then written into a separate file. Additionally, the CSV file listing all the bins is created in the same folder.

 1. Open the Maximum Intensity Projection (MIP) of 3D image stack or 2D image with ImageJ software
 2. Select Multi-point tool and put set of point pairs, to define the orientation of the bins. Attention, the total number of points, of course, should be even.
 3. Open the macros script and press run the script.

**Comments:**

* Before collecting profile information, Enhance Contrast and Subtract Background operations are applied to the image.

* The following parameters could be customly defined: 

> *rbr* = floor(20/voxelWidth); //Rolling Ball Radius, divided by voxelWidth because should be specified in pixels. 20um by default
> 
> *binWidth* = 300; //Width of the bin, 300um by default
> 
> *binLength* = 1500; //Length of the bin, 300um by default
> 
> *delay* = 700; //Delay between collecting new profile data, introduced due to ImageJ instability
> 
> *beforeP* = 20; //Length of the margin before the first user-defined point. 20um by default


**Second**, Python script is designed to build the 3D topographic profile for each consecutive graph. The script merges the extracted information from the folder with bin profiles in TXT files and a meta-data CSV into a single data-frame. By default, all profiles are interpolated to 1um step. This was made due to the need to process images with different resolution.

1. Prerequisites Python 3.5 + numpy + pandas + os + scipy.interpolate
2. In surfaceplot.py, set singleFolder to the folder where the profile bins have been stocked
3. Launch the script, the visualization is built using plotly extension


