'''
Created on Jun 6, 2012
Edited November 18, 2014 for Raichu probe, Guanqing Ou

@author: paszekm
'''
'''
The software is intended for analysis of FRET images.  The software assumes that for all FRET image sequences, image1 is the 
CFP channel, image2 is the CFP/YFP FRET channel, and image3 is the YFP channel.  The software is designed for both 8-bit and
16-bit images, with most of the testing being done with 16-bit tiffs encoded by imageJ. Images should be named with the convention:
base_name + sequence number + color channel number.  The sequence number and color channel number should have the format ##, starting 
with 00.  Background images should be saved in a folder path/background and FRET data images in a folder path/FRET and MASK data 
images in a folder path/MASK.

The user must edit the input information in the software indicated by #** comments

Two images are output following processing by the software.  The first output image
is the FRET/CFP ratio image and the second is the FRET/YFP ratio image.  The data is output into the folder path/output

More details about the software will be included as new features are developed and finalized
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


'''Helper Functions'''

#Convert an interger to a sequence sring
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
       
    
'''The main program'''

if __name__ == '__main__':
    pass

#Define the background images - the images of a blank area of the coverslip

#Specify the path to the data folder
#path = '/media/Linux Storage/MattR/FRET Analysis/61312 Tension Sensor/Analysis/TS_tailless/'
#path = '/media/Linux Storage/MattR/FRET Analysis/62712 FRET - rac and vinc mutants/Analysis_10a_T12_TS_WAFER_0011/'
#path = '/media/Linux Storage/MattR/FRET Analysis/62712 FRET - rac and vinc mutants/10a_TS_TL_Wafer/Analysis/'
path = '/home/gogqou/Documents/Research/2D3D/2014-11-18/'

#**Provide the base name of the background images 
#background_name = "Muc1-ATR TS-background"
background_name = 'TS_'

#**Provide the base name of the mask images
mask_name = 'masks' 

#**Enter the number of background image series - the number of spots on the coverslip imaged
background_num = 7

#**Specify the number of of pixels for the median filter used to smooth the background images
size_bfilter = 3

#**Provide the base name of the FRET data images
#image_name = "Muc1-ATR TS-"
image_name = 'TS_'

#**Enter the number of data image series - the number of spots on the coverslip imaged
image_num = 9

#**Provide the size (pixels x, pixels y) of the images
nrows=520
ncols=696
image_size = (nrows,ncols)

#**Provide the bleed through coefficient for FRET from the CFP alone
bleedCFP = 0.408

#**Provide the bleed through coefficient for FRET from the YFP alone
bleedYFP = 0.05

#**Specify the number of of pixels for the median filter used to smooth the data images
size_filter = 1

#Provide a multiplier for the output FRET to CFP ratio image
FRETtoCFP_mult = 1000

#Provide a multiplier for the output FRET to CFP ratio image
FRETtoYFP_mult = 1000

#Provide a cut off for the ratio images.  The cut off is how many times above the mean FRET ratio that
#pixels are included in the output
cutoff = 3

#Make any necessary folders
file_path = path + "background/processed"
if not os.path.isdir(file_path):
    os.makedirs(file_path)

file_path = path + "output/FRETtoCFP"
if not os.path.isdir(file_path):
    os.makedirs(file_path)
    
file_path = path + "output/FRETtoYFP"
if not os.path.isdir(file_path):
    os.makedirs(file_path)
    
file_path=path + 'maps/'
if not os.path.isdir(path + 'maps/'):
        os.makedirs(path + 'maps/')



'''for mapping'''
#minimum intensity to consider
minHeight=100

maxHeight=1000

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
lut_file_path = "/home/weaver/Desktop/LUT14.lut"

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

#Create an image of the background and store in the folder path/background/processed.
#Open the background images and create a running average of the images smoothed with a Median filter
bChannel1 = np.zeros((image_size[1],image_size[0]))
bChannel2 = np.zeros((image_size[1],image_size[0]))
bChannel3 = np.zeros((image_size[1],image_size[0]))
#print bChannel1.shape
#print bChannel1.dtype

#Open the background images and store the sum of their values in the appropriate bChannel matrix
for i in range(background_num):
    file_path = path + "background/" + background_name + sequenceNum(i) + "00.tif"
    im = Image.open(file_path)
    Temp = image2array(im)
    bChannel1 = bChannel1 + flts.median_filter(Temp, size_bfilter)
    
    file_path = path + "background/" + background_name + sequenceNum(i) + "01.tif"
    im = Image.open(file_path)
    Temp = image2array(im)
    bChannel2 = bChannel2 + flts.median_filter(Temp, size_bfilter)
    
    file_path = path + "background/" + background_name + sequenceNum(i) + "02.tif"
    im = Image.open(file_path)
    Temp = image2array(im)
    bChannel3 = bChannel3 + flts.median_filter(Temp, size_bfilter)
    
#Finish computing the averages for the background images
bChannel1 = bChannel1/background_num
bChannel2 = bChannel2/background_num
bChannel3 = bChannel3/background_num

#Save the background images
im = array2image(np.uint16(bChannel1))
im.save(path + "background/processed/bChannel00.tif")
im = array2image(np.uint16(bChannel2))
im.save(path + "background/processed/bChannel01.tif")
im = array2image(np.uint16(bChannel3))
im.save(path + "background/processed/bChannel02.tif")

#Process the data images
for i in range(image_num):
    print "Processing image #: ", i
    #Open the data images
    file_path = path + "FRET/" + image_name + sequenceNum(i) + "00.tif"
    im = Image.open(file_path)
    Channel1 = flts.median_filter(image2array(im), size_filter) - bChannel1  #The background corrected CFP channel
    
    file_path = path + "FRET/" + image_name + sequenceNum(i) + "01.tif"
    im = Image.open(file_path)
    Channel2 = flts.median_filter(image2array(im), size_filter) - bChannel2  #The background corrected FRET channel
    
    file_path = path + "FRET/" + image_name + sequenceNum(i) + "02.tif"
    im = Image.open(file_path)
    Channel3 = flts.median_filter(image2array(im), size_filter) - bChannel3   #The background corrected YFP Channel
    
    #Create the mask using the mask image
    #file_path = path + "masks/" + image_name + sequenceNum(i) + ".tif"
    file_path = path + "masks/" + mask_name + sequenceNum(i) + ".tif"
    #file_path = path + "masks/" + mask_name + sequenceNum(i) + ".png"
    im = Image.open(file_path)
    b = image2array(im)
    mask = (b == 0)
    
    
    
    
    '''Calculate the FRET'''
    FRET = np.zeros((image_size[1],image_size[0]))
    FRET[mask] = FRET[mask] + Channel2[mask] - bleedCFP*Channel1[mask] - bleedYFP*Channel3[mask]
    
    #Save the FRET ratio images
    Ratio = np.zeros((image_size[1],image_size[0]))
    Ratio[mask] = FRET[mask]/Channel3[mask]
    Ratio16 = np.uint16(Ratio*FRETtoYFP_mult)
    
    #eliminate any values that are above or below cutoff*mean
    cutoffValue=cutoff*Ratio16.mean()               
    cut = Ratio16 > cutoff*Ratio16[mask].mean()
    cut = Ratio16 > FRETtoYFP_mult #eliminate any FRET values above 100% FRET efficiency 
    Ratio16[cut] = 0
    im = array2image(Ratio16)
    file_path = path + "output/FRETtoYFP/FRETtoYFP" + sequenceNum(i)
    im.save(file_path + ".tif")
    #s = sp.surfacePlot(Ratio16, nrows, ncols, xyspacing, zscale, sequenceNum(i), plotRange, file_path + '_map' + surface_ext, lutfromfile, lut, lut_file_path, colorbar_on, save, view)
    np.savetxt((file_path + '.txt'), Ratio16, delimiter=' ')
    
    Ratio = np.zeros((image_size[1],image_size[0]))
    Ratio[mask] = FRET[mask]/Channel1[mask]
    Ratio16 = np.uint16(Ratio*FRETtoCFP_mult)
    cut = Ratio16 > cutoff*Ratio16[mask].mean()
    cut = Ratio16 > FRETtoCFP_mult #eliminate any FRET values above 100% FRET efficiency 
    Ratio16[cut] = 0
    im = array2image(Ratio16)
    file_path = path + "output/FRETtoCFP/FRETtoCFP" + sequenceNum(i)
    im.save(file_path + ".tif")
    s = sp.surfacePlot(Ratio16, nrows, ncols, xyspacing, zscale, sequenceNum(i), plotRange, file_path + '_map' + surface_ext, lutfromfile, lut, lut_file_path, colorbar_on, save, view)
    np.savetxt((file_path + '.txt'), Ratio16, delimiter=' ')
    
    
    
    '''Record extra information from FRET to CFP channel'''
    RatiosOnly=[]
    for i in range(ncols):
        for j in range(nrows):
            if Ratio16[i,j] < 0:
                Ratio16[i,j] = 0
            #Save an array of positive heights only
            if Ratio16[i,j] > 0:
                RatiosOnly.append(Ratio16[i,j])
    
    
    #Get mean and standard deviation and gaussian fit from Heights
    RatiosOnly=array(RatiosOnly)
    np.savetxt((file_path + 'RatiosOnly' + '.txt'), Ratio16, delimiter=' ')
    print 'n= ', len(RatiosOnly)
    print 'mean= ', RatiosOnly.mean()
    print 'std= ', RatiosOnly.std()
    mean.append(RatiosOnly.mean())
    std.append(RatiosOnly.std())
    n.append(len(RatiosOnly))
    print ''
    
#Save n,mean,std and name_list to txt file
n=array(n)
mean=array(mean)
std=array(std)
file_path = path + "output/FRETtoCFP/FRETtoCFP"
np.savetxt((file_path + 'n.txt'), n, delimiter=' ')
np.savetxt((file_path + 'mean.txt'), mean, delimiter=' ')
np.savetxt((file_path + 'std.txt'), std, delimiter=' ')    
#name_list has to be altered separately to have 'newline' characters, in order to write to a file
    
print "FRET analysis complete"

    