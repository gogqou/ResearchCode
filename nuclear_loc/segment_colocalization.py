'''
Created on May 2, 2014

@author: gogqou
'''

import numpy as np
from collections import defaultdict
def compareArraysOLD(segmented_array_dictionary, coloc_dictionary, segment_sizes_dict, overlap_threshold, dims):
    s_dict = segmented_array_dictionary
    col_dict=coloc_dictionary
    dim1=dims[0]
    dim2=dims[1]
    #coloc_array_segmented = np.zeros((dim1,dim2))
    segment_count = defaultdict(int)
    for k,v in s_dict.iteritems():
        if k in col_dict.keys():            
            segment_count[str(v)]+=1
            print k
    return segment_count
def compareArrays(segment_array, coloc_array):
    print 'compareArrays'
    dims=segment_array.shape
    dim1=dims[0]
    dim2=dims[1]
    new_coloc_array = np.zeros(dims)
    segment_count = defaultdict(int)
    for i in range(dim1):
        for j in range(dim2):
            if segment_array[i,j]!=0 and coloc_array[i,j]!=0:
                segment_count[str(segment_array[i,j])]+=1
                new_coloc_array[i,j]=segment_array[i,j]
                #print coloc_array[i,j] 
            else:
                new_coloc_array[i,j]=0
    return segment_count, new_coloc_array
def compareOverlap(segment_sizes, segment_count, threshold=.3):
    print 'compareOverlap'
    positive_segments = []
    for k, v in segment_sizes.iteritems():
        print k, segment_count[k], v,float(segment_count[k])/float(v)
        
        if float(segment_count[k])/float(v)>=float(threshold):
            print k, segment_count[k]/v
            positive_segments.append(k)
    return positive_segments
        