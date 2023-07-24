# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 11:29:57 2023

@author: smdb
"""

#Importing python libraries to be used
import os
import shutil
import glob
import time
from os.path import basename,join,getmtime

#Inserting the path to the log file
report = input('Enter the path to the log file: ')
print(report)
if os.path.exists(report):
    print('The directory exists')

#Opening the log file and writting the operations
with open(report, 'w') as f:
    
    
    #Inserting the path to the source folder
    path_source_initial = input('Enter the path to the source folder: ')
    print(path_source_initial)
    if os.path.isdir(path_source_initial):
        print('The directory exists')
    
    #Inserting the path to the replica folder
    path_replica_initial = input('Enter the path to the replica folder: ')
    print(path_replica_initial)  
    if os.path.isdir(path_replica_initial):
        print('The directory exists')
    
    #Inserting the syncronization time in seconds
    refresh_rate = None
    while refresh_rate is None:
        try:
            refresh_rate=int(input("Please enter the syncronization time in seconds:"))
        except ValueError:
            print("Invalid integer!")
    
    #Creating lists of initial content in the source and replica folders
    list_filenames_source_zero = glob.glob(join(path_source_initial,"*"),recursive=True)
    list_filenames_replica_zero = glob.glob(join(path_replica_initial,"*"),recursive=True)   
   
    #Condition that compares the amount of files in the initial source and replica folders and copies the initial files.  
    if len(set(list_filenames_source_zero))!=0 and len(set(list_filenames_replica_zero))==0:
        [shutil.copy(x,join(path_replica_initial,basename(x))) for x in list_filenames_source_zero]
        print ("Initial update done")
        print ("Initial update done",file=open(report, 'a'))
        
    
    #Creating lists using the basenames in the initial source and replica folders.    
    list_basenames_source = [basename(i) for i in list_filenames_source_zero]
    list_basenames_replica = [basename(i) for i in list_filenames_replica_zero]
    
    
    #Replacing the basenames in the replica folder.
    if len(list(set(list_basenames_source) - set(list_basenames_replica)))!=0:
        old_basenames = (list(set(list_basenames_replica) - set(list_basenames_source)))
        new_basenames = (list(set(list_basenames_source) - set(list_basenames_replica)))
        [os.rename(join(path_replica_initial,basename(old)),join(path_replica_initial,basename(new)))
             for (old,new) in zip(old_basenames,new_basenames)]
        print ("Initial basenames updated")
        print ("Initial basenames updated", file=open(report, 'a'))
     
    #Declaring a variable that returns the local time.    
    local_float_zero = time.time()
    
    
    while True:
        
        #Creating lists of content in the source and replica folders.
        list_filenames_source = glob.glob(join(path_source_initial,"*"),recursive=True)
        list_filenames_replica = glob.glob(join(path_replica_initial,"*"),recursive=True)
        print("Count of elements in source:",len(list_filenames_source))
        print("Count of elements in replica:",len(list_filenames_replica))
        print("Count of elements in source:",len(list_filenames_source),file=open(report, 'a'))
        print("Count of elements in replica:",len(list_filenames_replica),file=open(report, 'a'))
        
         
        if set(list_filenames_source_zero) != set(list_filenames_source):
            #Removing files to the replica folder that have been deleted in the source folder.
            if len(set(list_filenames_source_zero)) > len(set(list_filenames_source)):
                removing_files=list(set(list_filenames_source_zero) - set(list_filenames_source))
                [os.remove(join(path_replica_initial,basename(x))) for x in removing_files]
                print ("Files removed successfully:", removing_files)
                print ("Files removed successfully:", removing_files, file=open(report,'a'))
                
            #Copying files to the replica folder that have been created in the source folder.    
            if len(list_filenames_source_zero) < len(list_filenames_source):
                copying_files=list(set(list_filenames_source) - set(list_filenames_source_zero))
                [shutil.copy(x,join(path_replica_initial,basename(x))) for x in copying_files]
                print ("Files copied successfully:", copying_files)
                print ("Files copied successfully:", copying_files, file=open(report,'a'))
         
        #Replacing the basenames in the replica folder.        
        if len(list(set(list_filenames_source_zero) - set(list_filenames_source)))!=0:
            old_basenames = (list(set(list_filenames_source_zero) - set(list_filenames_source)))
            new_basenames = (list(set(list_filenames_source) - set(list_filenames_source_zero)))
            [os.rename(join(path_replica_initial,basename(old)),join(path_replica_initial,basename(new)))
             for (old,new) in zip(old_basenames,new_basenames)]
            print("Basenames updated")
            print("Basenames updated", file=open(report,'a'))
            
            
            
        list_filenames_source_zero = list_filenames_source
        local = time.localtime()
        local_float = time.time()
        
        #Copying the modified files from the source to the replica folder.
        for file in list_filenames_source:
            modification_time = getmtime(file)
            if local_float_zero<modification_time:
                shutil.copy(file,join(path_replica_initial,basename(file)))
                print("Modified files updated successfuly")
                print("Modified files updated successfuly", file=open(report,'a'))
                
                
        result= time.strftime("%Y:%M:%S",local)
        print("Update done at:",result)
        print("Update done at:",result, file=open(report,'a'))
        time.sleep(refresh_rate)
        local_float_zero = local_float

f.close()



