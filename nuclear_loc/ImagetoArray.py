'''
Created on May 2, 2014

@author: gogqou
'''


from ImageStackgou import *
def processImage(home_dir, basename, imageext):
    #populate the stack based on the provided directory, basename, number of images per stack, and their image extension
    im=Image_gou(home_dir+ basename+ imageext)
    
    return im.array