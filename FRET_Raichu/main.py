'''
Created on Nov 19, 2014

@author: gogqou
'''
import numpy as np
import pylab as py
import csv
from scipy.optimize import leastsq
import Image
import os as os
import scipy.ndimage.filters as flts
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.special import erfc
from scipy.special import erf
import surfacePlot as sp
from numpy import *

import ImageDraw
import Image
import random
'''Helper Functions'''

#Convert an integer to a sequence sring
def sequenceNum(n):
    if n < 10:
        return "0" + str(n)
    else:
        return str(n)

#convert image into array according to im.mode - Still in development
def image2arrayFast(im):
    if im.mode in ("L",):
        return np.reshape(np.fromstring(im.tostring(), np.uint8), (im.size[1],im.size[0]))
    elif im.mode in ("I;16",):
        return np.reshape(np.fromstring(im.tostring(), np.uint16), (im.size[1],im.size[0]), order='A')
    elif im.mode in ("I;16B",):
        Temp = np.reshape(np.fromstring(im.tostring(), np.uint16), (im.size[1],im.size[0]))
        Temp2 = np.float64(Temp)
        return Temp2
        #return np.reshape(np.fromstring(im.tostring(), np.uint16), (im.size[1],im.size[0]))
    else:
        print "here"

#convert image into array
def image2array(im):
    pix = im.load()
    a = np.zeros((im.size[1], im.size[0]))
    for i in range(im.size[1]):
        for j in range(im.size[0]):
            a[i,j] = pix[j,i]
    return a
            

#convert array into image according to a.dtype
def array2image(a):
    if a.dtype == np.uint8: 
        mode = "L"
    elif a.dtype == np.uint16: 
        mode = "I;16"
    else:
        raise ValueError, "unsupported image mode"
    return Image.fromstring(mode, (a.shape[1],a.shape[0]), a.tostring())


    
    
    return 1

'''The main program'''


if __name__ == '__main__':
    pass

#Define the background images - the images of a blank area of the coverslip

#Specify the path to the data folder
path = '/home/gogqou/Documents/Research/2D3D/2014-11-18/Analysis/Rac_inh/'

#**Provide the base name of the background images 
#background_name = "Muc1-ATR TS-background"
background_name = 'BG_'

#**Specify the number of of pixels for the median filter used to smooth the background images
size_bfilter = 3

#**Provide the base name of the mask images
mask_name = 'mask' 

#**Enter the number of background image series - the number of spots on the coverslip imaged
background_num = 7


#**Provide the base name of the FRET data images
#image_name = "Muc1-ATR TS-"
image_name = 'Raichu_Rac_inhib_FYC_30min_'
#image_name = 'Raichu_test_FYC_'

#**Enter the number of data image series - the number of spots on the coverslip imaged
image_num = 1
#**Provide the size (pixels x, pixels y) of the images
nrows=1392
ncols=1040
image_size = (nrows,ncols)



#**Specify the number of of pixels for the median filter used to smooth the data images
size_filter = 1

#Provide a multiplier for the output FRET to CFP ratio image
FRETtoCFP_mult = 1000

#Provide a multiplier for the output FRET to CFP ratio image
FRETtoYFP_mult = 1000


'''for mapping'''
#minimum intensity to consider
minHeight=800

maxHeight=1050

xyspacing = 110  #was 0.45
    
#modify this parameter if you wish to change the z-scaling (height) relative to the xy-scaling
zscale = 0 #40 #80 for microtubule
    
#The range of the colormap for the z heights
plotRange = [minHeight,maxHeight]
    
#The range of z heights to include in the graphing
hRange = [minHeight,maxHeight]

#True if the colormap will come from a file
lutfromfile = True
    
#Color map file path
lut_file_path = "/home/gogqou/Desktop/LUT14.lut"

#The colormap if a built in one is used (mapfromfile = 'False')
lut="gist_stern"
    
#Set to true if you want a colorbar on your image.  Otherwise set to False
colorbar_on = True
    
#View figure - set this option to true if you would like to view and modify the surface plot and then manually save it
view = False
    
#Save Figure? - Set this option to false if you plan on viewing the surface plot, manually adjusting it, and saving it
save = True
    
#The desired file extension for the save surface plot - can be .jpg, .png, .tif, etc.  The reconstruction will be saved as this file type
surface_ext = '.png'

#create empty mean, std, and n=count arrays
mean=[]
std=[]
n=[]



"""All the required information has now been specified - It is time to start processing the data"""
#Create the mask using the mask image
#file_path = path + "masks/" + image_name + sequenceNum(i) + ".tif"
file_path = path + image_name + '001_'  + "mask.tif"
#file_path = path + "masks/" + mask_name + sequenceNum(i) + ".png"
im = Image.open(file_path)
b = image2array(im)
mask = (b == 0)
#bChannelYFP = np.ones((image_size[1],image_size[0]))*190
#bChannelCFP = np.ones((image_size[1],image_size[0]))*200

file_path = path + image_name + '001_' + "YFP.tif"
im = Image.open(file_path)
FRET_channel = flts.median_filter(image2array(im), size_filter)

file_path = path + image_name + '001_' + "CFP.tif"
im = Image.open(file_path)
CFP_channel = flts.median_filter(image2array(im), size_filter)


file_path = path + image_name + '001_' + "YFPorig.tif"
#im = Image.open(file_path)
#YFP_channel = flts.median_filter(image2array(im), size_filter)


Ratio = np.zeros((image_size[1],image_size[0]))
Ratio[mask] = FRET_channel[mask]/CFP_channel[mask]
print Ratio[488]
print np.amax(Ratio)
print np.amin(Ratio)
Ratio16 = np.uint16(Ratio*FRETtoYFP_mult)

im = array2image(Ratio16)

file_path = path + "YFPtoCFP" + image_name+'001_'
im.save(file_path + ".tif")
print Ratio16[488]

#The range of the colormap for the z heights
minHeight = FRETtoYFP_mult*np.amin(Ratio)
maxHeight= FRETtoYFP_mult*np.amax(Ratio)
#plotRange = [minHeight,maxHeight]

s = sp.surfacePlot(Ratio16, nrows, ncols, xyspacing, zscale, '001_', plotRange, file_path + '_map' + surface_ext, lutfromfile, lut, lut_file_path, colorbar_on, save, view)
np.savetxt((file_path + '.txt'), Ratio16, delimiter=' ')
print "FRET analysis complete"

               