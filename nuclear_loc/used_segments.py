'''
Created on May 7, 2014

@author: gogqou
'''
import numpy as np
def newSegmentArray(positive_segments, original_array):
    print 'newSegmentArray'
    dims = original_array.shape
    dim1 = dims[0]
    dim2 = dims[1]
    
    newArray=np.zeros(dims)
    newArray2=np.zeros(dims)
    for i in range(dim1):
        for j in range(dim2):
            if original_array[i,j]==0:
                newArray2[i,j]= 2
            elif str(original_array[i,j]) in positive_segments:
                newArray[i,j] = original_array[i,j]
                #print original_array[i,j]
                newArray2[i,j]= 1
    return newArray, newArray2