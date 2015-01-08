'''
Created on Dec 11, 2013

@author: gou
'''
import os
import csv
import numpy as np

def readcsv(filename):
    print filename
    f=open(filename,'rb')
    lines = f.readlines()
    size =[5768,7082]
    csv_data= np.zeros(size)
    
    #enumerate numbers the lines, the 1 specifies that n starts at 1 instead of 0   
    for n, line in enumerate(lines, 1):
    
        #strips away the \n delimiter at end of each line that makes a new line
        lineagain = line.rstrip()
        #uses ',' as delimiter to separate out the relevant information
        line_split = lineagain.split(',')
        
        csv_data [n-1,:] = line_split        
   
    return csv_data
def writecsv(array,end_dir,outputname):
    
    #change the directory
    os.chdir(end_dir)
    #open the file 
    f = open(outputname, 'wb')
    #create a writer object
    writer = csv.writer(f)
    
    #iterate through each row of the array and populate a matrix 
    #corresponding to the data in the array
    for i in range(len(array)):
        writer.writerow(array[i,:])
    return 1

def writetxt(array, end_dir, outputname):
    
    
    return 1