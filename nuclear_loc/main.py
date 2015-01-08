'''
Created on May 1, 2014

@author: gogqou
'''
import sys
from ImageStackgou import *
import Image
import zproject as zp 
import segmentation_watershed as seg_wt
import readwrite_file as rd_wrt
import os
import draw_segment_image as draw
import calc_segment_size as seg_size
import ImagetoArray as ItA
import segment_colocalization as seg_col
import used_segments as u_seg

def processStack(home_dir, basename, imageext, heightsdir, num = None):
    if num is None:
        num = 6
    #populate the stack based on the provided directory, basename, number of images per stack, and their image extension
    stack=Stack_gou(home_dir, num, basename, imageext)
    #calls zproject to produce an average-intensity value for the stack
    zprojected =  zp.zproject(stack)
    #saves this image
    name =home_dir+basename+'_zprojected'+imageext
    
    plt.imsave(name, zprojected)
    
    #converts zprojected image to greyscale in preparation for segmentation
    image=Image.open(name).convert('L')
    #implements watershed segmentation from the mahotas/pymorph computer vision library
    #*after contrast enhancement and gaussian blurring -- can change
    
    #add option = 'contrast' if want to run contrast enhancement on image before processing
    #otherwise there will only be Gaussian filtering
    print 'about to segment'
    nuclei_array_labels, num_adhesions=seg_wt.segmentation(image, home_dir, basename)
    
    #the output of segmentation is a csv of numbers corresponding with pixels in the original image
    #if a pixel was found to belong to a segment, or nucleus
    #it was a number that groups with all other pixels in that adhesion
    #if not, it will have a value of 0
    rd_wrt.writecsv(nuclei_array_labels,home_dir, 'nuclei_nums.csv')
    return nuclei_array_labels


def process_Thresholded_image(home_dir, basename, imageext):
    name=home_dir+basename+imageext
    #converts zprojected image to greyscale in preparation for segmentation
    image=Image.open(name).convert('L')
    #implements watershed segmentation from the mahotas/pymorph computer vision library
    #*after contrast enhancement and gaussian blurring -- can change
    
    #add option = 'contrast' if want to run contrast enhancement on image before processing
    #otherwise there will only be Gaussian filtering
    print 'about to segment'
    nuclei_array_labels, num_adhesions=seg_wt.segmentation(image, home_dir, basename)
    
    #the output of segmentation is a csv of numbers corresponding with pixels in the original image
    #if a pixel was found to belong to a segment, or nucleus
    #it was a number that groups with all other pixels in that adhesion
    #if not, it will have a value of 0
    rd_wrt.writecsv(nuclei_array_labels,home_dir, basename+'nuclei_nums.csv')
    return nuclei_array_labels
    
    
def draw_image(home_dir, basename,addname, array):
    
    png_output_name = home_dir+basename+addname+'.bmp'
    #scalingFactor makes the numbers and adhesions easier to see
    #depends on how big your original image is and how big the segments are
    #try out diff scalingFactors to see result
    #this function also has the option of picking a minimum adhesion size
    #default = 1
    #change by adding minClump = ##, where ## = # pixels 
    print 'drawing segmented image'
    draw.makeImage(png_output_name, array, scalingFactor = 2)

def main():
    if len(sys.argv)<8:
        print 'not enough inputs--please enter source directory, data set name, base filename,  image extension, and heights directory\nfor example: "/home/Documents/Images/", cell1, _c, .tif, /home/Documents/Images/'
        sys.exit()
    elif len(sys.argv)>8:
        print 'too many inputs, only used first five'
        
    directory=sys.argv[1] 
    dataset = sys.argv[2]
    basename = sys.argv[3]
    imageext = sys.argv[4]
    heightsdir = sys.argv[5]
    threshold = sys.argv[6]
    overlap_threshold=sys.argv[7]
    
    #array=processStack(directory, dataset+basename, imageext, heightsdir)
    
    #array=process_Thresholded_image(directory,dataset+basename,imageext)
    array = rd_wrt.readcsv(directory+dataset+basename+'nuclei_nums.csv')
    #draw_image(directory,dataset+basename,'_nuclei', array)
    #[segment_pixel_dictionary, segment_sizes]=pop_dict.array_to_dict_segment(array,'nucleus')
    
    
    green_channel = ItA.processImage('/home/gogqou/Documents/Research/Ori/4LMG_#15_2_h/','C2_4LMG_15_60X_R_1_1', '.tif')
    print green_channel[1:10]
    green_channel[green_channel<int(threshold)]=0
    print green_channel[1:10]
    segment_sizes= seg_size.array_to_dict_segment(array, 'coloc_signal')
    
    [segment_count, new_coloc_array]=seg_col.compareArrays(array, green_channel)
    draw_image(directory,dataset+basename+'signal_used','green_channel', new_coloc_array)
    #for k,v in segment_count.iteritems():
        #print k,v
    
    positive_nuclei=seg_col.compareOverlap(segment_sizes,segment_count,overlap_threshold)
    #print positive_nuclei
    print len(positive_nuclei)
    positive_nuclei = sorted(positive_nuclei)
    
    print positive_nuclei
    
    [new_nuclei, binary_nuclei] = u_seg.newSegmentArray(positive_nuclei, array)
    #draw_image(directory,dataset+basename+'positive', '_nuclei', new_nuclei)
    draw_image(directory,dataset+basename+'positive', '_nuclei_binary', binary_nuclei)
    print 'done'
    #print max(segment_count.keys())
    
    '''    
    home_dir=sys.argv[1] 
    dataset = sys.argv[2]
    basename = sys.argv[3]
    imageext = sys.argv[4]
    heightsdir = sys.argv[5]
    
    folders = os.listdir(home_dir)
    '''
    '''
    #cycles through folders and analyzes each stack within the subfolders
    for folder in folders:
        #practical processes to get the right directory to feed into processStack
        directory = home_dir + folder + '/'
        newbasename = dataset +folder+basename
        new_heightsdir = heightsdir + dataset+'/'+folder+'/'
        print 'processing ' + newbasename + ' in ' + new_heightsdir
        
        processStack(directory, newbasename, imageext, new_heightsdir)
        
    ''' 
    #compilef.move(home_dir,'histogram', home_dir)

if __name__ == '__main__':
    main()