import numpy as np
import scipy.io as sio
import random
import os
import shutil
from shutil import copyfile
import time
base_dir = "PATH TO YOUR BITVehicle_Dataset FOLDER" #C:/users/username/downloads/Matlab to txt via python/BITVehicle_Dataset

def mymovefile(srcfile,dstfile):

    if not os.path.isfile(srcfile):

        print ("%s not exist!"%(srcfile))

    else:

        fpath,fname=os.path.split(dstfile)    

        if not os.path.exists(fpath):

            os.makedirs(fpath)                

        shutil.move(srcfile,dstfile)         

        print ("move %s -> %s"%( srcfile,dstfile))


load_fn = base_dir + 'VehicleInfo.mat'

load_data = sio.loadmat(load_fn)


data = load_data['VehicleInfo']

# Line below will create a 1500 images for test set if you want more or less change the "1500" value below to your desire
test_index = random.sample(range(data.size), 1500) 

for i in range(2):
    item = data[i]
    str = ""
    for j in range(item['vehicles'][0][0].size):
    # print '**************************'
    
        name = item['name'][0][0]

        # Bus, Microbus, Minivan, Sedan, SUV, and Truck

        vehicles = item['vehicles'][0][0][j]
        height = item['height'][0][0][0]

        width = item['width'][0][0][0]

        left = vehicles[0][0][0]

        top = vehicles[1][0][0]

        right = vehicles[2][0][0]

        bottom = vehicles[3][0][0]

        vehicles_type = vehicles[4][0]

        if(vehicles_type == 'Bus'): vehicles_type = 0

        elif(vehicles_type == 'Microbus'): vehicles_type = 1

        elif(vehicles_type == 'Minivan'): vehicles_type = 2

        elif(vehicles_type == 'Sedan'): vehicles_type = 3

        elif(vehicles_type == 'SUV'): vehicles_type = 4

        elif(vehicles_type == 'Truck'): vehicles_type = 5

        str += '%s %s %s %s %s' %(vehicles_type, round(float( (left + (right-left)/2)/width),6) , round(float((top + (bottom-top)/2)/height),6),  round(float((right-left)/width),6), round(float((bottom-top)/height),6))+'\n'
        
    str = str[:str.rfind('\n')]
    print (str)
    if(i in test_index):
        with open("PATH TO Matlab to txt via python"+name[:-3]+"txt", 'a+') as f: #C:/users/username/downloads/Matlab to txt via python
            f.write(str + '\n')
            f.close()
        str = '%s%s' %("data/test/", name)
        with open(base_dir+"test.txt",'a+') as t:
            t.write(str + '\n')
            t.close()  
            copyfile(base_dir + "dataset/" + name, base_dir + "test/"+ name)
            mymovefile("PATH TO Matlab to txt via python" + name[:-3]+"txt", base_dir + "val/") #C:/users/username/downloads/Matlab to txt via python
    else:
        with open(base_dir+name[:-3]+"txt", 'a+') as f:
            f.write(str + '\n')
            f.close()
        str = '%s%s' %("data/vehicle/", name)
        with open(base_dir+"train.txt",'a+') as t:
            t.write(str + '\n')
            t.close()  
            copyfile(base_dir + "dataset/" + name, base_dir + "train/"+name)
            mymovefile(base_dir + name[:-3]+"txt", base_dir + "train/")        
print ('done--')
