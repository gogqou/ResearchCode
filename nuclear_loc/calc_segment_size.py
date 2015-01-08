'''
Created on May 1, 2014

@author: gogqou
'''
from collections import defaultdict
def array_to_dict_segment(array,entry_type):
    #entry_type is what the label for the entries in the dictionary are
    #for instance, "adhesion", "segment", "nucleus","cell"
    #array is the array that we cycle through and 
    size=array.shape 
    dim1 = size[0]
    dim2 = size[1]
    print dim1, dim2
    segment_sizes = defaultdict(int)
    for i in range(dim1):
        for j in range(dim2):
            if array[i,j]==0:
                continue
            else:
                segment_sizes[str(array[i,j])]+=1
                #print segment_sizes[str(array[i,j])]
                
    return segment_sizes

