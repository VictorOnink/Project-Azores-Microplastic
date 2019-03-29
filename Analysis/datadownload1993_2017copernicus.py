# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 09:47:10 2018

@author: Victor Onink
Downloading the 3h resolution total currents, but from Copernicus instead of the 
GlobCurrent server
"""
import urllib
import numpy as np
import datetime

#testfile = urllib.URLopener()
#testfile.retrieve(url, "D:\Desktop\Thesis/works.nc")
#dataset-uv-rep-hourly_20170101T0000Z_P20180501T0000Z_P20180501T0000Z.nc
direc='ftp://my.cmems-du.eu/Core/MULTIOBS_GLO_PHY_REP_015_004/dataset-uv-rep-hourly' 
savedirec='/alphadata04/onink/lagrangian_sim/GlobCurrent1993_2017'
s='/' #this marks the directories, not \ since that fails with numbers in the directory names
prefix='dataset-uv-rep-hourly_'
suffix='T0000Z_P20180501T0000Z_P20180501T0000Z.nc'
for i in range(1993,2018):
        direcyear=direc+s+str(i)
        if i==1996 or i==2000 or i==2004 or i==2008 or i==2012 or i==2016:
            days=366
        else:
            days=365
        if i==2000:
            start=1
        else:
            start=1
        for j in range(start,days+1):
            if j<10:
                day='00'+str(j)
            elif j>=10 and j<100:
                day='0'+str(j)
            else:
                day=str(j)
            Date=datetime.datetime(i, 1, 1) + datetime.timedelta(j - 1)
            [y, m, d]=[Date.year,Date.month,Date.day]
            if m<10:
                if d<10:
                    direcday=direcyear+s+'0'+str(m)+s
                    datestamp=str(y)+'0'+str(m)+'0'+str(d)
                else:
                    datestamp=str(y)+'0'+str(m)+str(d)
                    direcday=direcyear+s+'0'+str(m)+s
            else:
                if d<10:
                    datestamp=str(y)+str(m)+'0'+str(d)
                    direcday=direcyear+s+str(m)+s
                else:
                    datestamp=str(y)+str(m)+str(d)
                    direcday=direcyear+s+str(m)+s
            File=direcday+prefix+datestamp+suffix
            SaveName=savedirec+s+prefix+datestamp+suffix
#            testfile = urllib.URLopener()
#            testfile.retrieve(File, SaveName)
