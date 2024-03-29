# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 09:47:10 2018

@author: Victor Onink
Downloading the 3h resolution total currents
"""
import urllib
import numpy as np
import datetime

#testfile = urllib.URLopener()
#testfile.retrieve(url, "D:\Desktop\Thesis/works.nc")

direc='http://www.ifremer.fr/opendap/cerdap1/globcurrent/v3.0/global_025_deg/total_hs' 
savedirec='/scratch/Victor/TotalData'
s='/' #this marks the directories, not \ since that fails with numbers in the directory names
standard='-GLOBCURRENT-L4-CUReul_hs-ALT_SUM-v03.0-fv01.0.nc'
for i in range(1993,2018):
        direcyear=direc+s+str(i)
        if i==1996 or i==2000 or i==2004 or i==2008 or i==2012 or i==2016:
            days=366
        if i==2017:
            days=135 #since currently this is as far as the Globcurrent dataset goes
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
            direcday=direcyear+s+day+s
            Date=datetime.datetime(i, 1, 1) + datetime.timedelta(j - 1)
            [y, m, d]=[Date.year,Date.month,Date.day]
            if m<10:
                if d<10:
                    datestamp=str(y)+'0'+str(m)+'0'+str(d)
                else:
                    datestamp=str(y)+'0'+str(m)+str(d)
            else:
                if d<10:
                    datestamp=str(y)+str(m)+'0'+str(d)
                else:
                    datestamp=str(y)+str(m)+str(d)
            time=['000000','030000','060000','090000','120000','150000',
                  '180000','210000']
	    print i, j
            for k in range(len(time)):
                File=direcday+datestamp+time[k]+standard
		#if i==2013 and j==160 and k==6:
		 #   File='http://www.ifremer.fr/opendap/cerdap1/globcurrent/v2.0/global_025_deg/total_hs/20130609180000-GLOBCURRENT-L4-CUReul_hs-ALT_SUM-v02.0-fv01.0.nc'
                SaveName=savedirec+s+datestamp+time[k]+standard
	#	print time[k]
                testfile = urllib.URLopener()
                testfile.retrieve(File, SaveName)
