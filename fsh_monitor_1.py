# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 08:38:33 2015

@author: lkock
C:\Users\Public\Documents\Rohde-Schwarz\FSH4View\gsm3
"""
#filename="Sweep 0001 (2015-11-17 11.21.12 AM).csv"

import os
import glob
import csv
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from Tkinter import Tk
from tkFileDialog import askopenfilename
import time as tt
import numpy as np



#open antenna cal file
antenna = askopenfilename(title="Select Antenna Cal File",initialdir=(os.path.expanduser("C:\RFI Archive\Equipment_Database\Passive_Antennas"))) # show an "Open" dialog box and return the path to the selected file
antenna_cal = loadtxt(antenna,delimiter=',',usecols=range(0,4),skiprows=1)

def movingaverage(interval, window_size):
    window= np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')
    
def detect(f, data_mat, det_thresh, window):
    fn_out=np.zeros(np.shape(data_mat))
    detect_f=np.zeros(np.shape(data_mat))
    for x in range(len(data_mat[:,1])):
        fn_out[x,:]=movingaverage(data_mat[x,:],window)+det_thresh
        detect_f[x,0:len(data_mat[x,data_mat[x,:]>fn_out[x,:]])]=f[data_mat[x,:]>fn_out[x,:]]
    return detect_f, fn_out 

def read_fsh_file():
    x=0
    dbm=np.zeros(shape=(len(glob.glob('*.csv')),631))
    
    time=[{}]*len(glob.glob('*.csv'))
    time2=np.empty([len(glob.glob('*.csv')),1])
    
    for filename in glob.glob('*.csv'):
        data = np.loadtxt(filename,delimiter=',',usecols=range(0,2),skiprows=46)
        af=np.interp(data[:,0],antenna_cal[:,1],antenna_cal[:,3])  
        time[x]=filename[12:31]
        time2[x]=(datestr2num(filename[23:31].replace('.',':')))
        dbm[x]=data[:,1]+107+af
        f=data[:,0]
        x=x+1
        os.remove(filename)
    
    return  f, dbm, time, time2
    

def plotte(f,dbm):
    subplot(121)
    imshow(dbm, aspect='auto')
    title("Measured E-field vs position and frequency")
    
    xticks(arange(0,len(f),len(f)/6),arange(min(f)/1e6,max(f)/1e6,10))
#    t_ind=arange(0,len(dbm),len(dbm)/10)
#    yticks(t_ind,geo[1:len(dbm):len(dbm)/10])
    
    colorbar()
    xlabel('Frequency MHz')
    
#    subplot(122)
#    hist(f_max,60e6/200e3)
#    grid()
#    xlabel('Frequency MHz')
#    title("Histogram of frequencies of Max E Fields in band")

#Process files that were logged prior to start
#f, out, time, time2=read_fsh_file()
#try:
#    f, out, time, time2=read_fsh_file()
#except:
#    print 'No files... Waiting'


#live update
out=np.zeros(shape=(1,631))
try:

    while True:
        print glob.glob('*.csv')
        try:
            f1, dbm1, time1, time21=read_fsh_file()
            tt.sleep(1)
            out=append(out,dbm1,axis=0)
#            time=append(time,time1,axis=0)
#            time2=append(time2,time21,axis=0)
            
        except:
            print 'No files...Waiting for update'
            tt.sleep(1)
        
            
except KeyboardInterrupt:
    print "zapped"

plotte(f1,out)
ff, detec = detect(f1, out, 3, 200)
#f=data[:,0]
#plt.figure()
#
#
#plotte(f,dbm)