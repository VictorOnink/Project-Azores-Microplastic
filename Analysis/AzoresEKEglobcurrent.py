# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 15:44:40 2019

@author: mrCle
I want to see if there is any match between when Catharina found abnormally high
microplastic counts and the EKE around the Azores

The definition of the azores area follows that of wikipedia...
24.5-31.5 W, 36.5-40.0 N

"""
import numpy as np
from netCDF4 import Dataset
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import geopy.distance as dis
import math
import pandas as pd
import matplotlib.dates as mdates


earth_radius = 6371.0 #km
degrees_to_radians = math.pi/180.0
radians_to_degrees = 180.0/math.pi

def change_in_latitude(km):
    "Given a distance north, return the change in latitude."
    return (km/earth_radius)*radians_to_degrees

#%%First, I need to have all the non-event days
excel='D:\Desktop\Bern Projects\Azores Microplastic Origin/2019_CPieper_non-event_days.xlsx'
FileEx=pd.read_excel(excel)
normEv=FileEx['Date dd/mm/yy'].astype('|S')
normEvDates=[]
for i in range(len(normEv)):
    date=datetime.strptime(normEv[i],'%Y-%m-%d')
    date=date.replace(minute=0)
    normEvDates.append(date)
    
#%% Next, I need to have the event days
excel='D:\Desktop\Bern Projects\Azores Microplastic Origin/2018_CPieper_modellingAzores_events.xlsx'
FileEx2=pd.read_excel(excel)
specEv=FileEx2['Date'].astype('|S')
source=FileEx2['Information Source'].astype('|S')
Notes=FileEx2['Notes'].astype('|S')
specEvDates=[]
for i in range(len(specEv)):
    if source[i]=='Photo DataBase' or source[i]=='Field Survey DataBase':
        if 'accumulation' in Notes[i]:
            date=datetime.strptime(specEv[i],'%Y-%m-%d')
            date=date.replace(minute=0)
            specEvDates.append(date)

#%%Finally, I need to get the EKE, which I should have in my files
azoresEKE=[]
azoresEKEtime=[]
for k in range(2010,2019):
    for m in range(1,13):
        if m<10:
            month='0'+str(m)
        else:
            month=str(m)
        File='D:\Desktop\Bern Projects\Azores Microplastic Origin\EKE\globCurrentEKE-'+str(k)+'-'+month+'.nc'
        dataset=Dataset(File)
        lon=dataset.variables['longitude'][593:622]
        lat=dataset.variables['latitude'][461:476]
        time=dataset.variables['time'][:]
        EKE=dataset.variables['EKE'][:,461:476,593:622]
        EKE[EKE==0.5]=np.nan
        for i in range(len(time)):
            azoresEKEtime.append(datetime(1950,1,1,0,0)+timedelta(hours=time[i]))
            azoresEKE.append(np.nanmean(EKE[i,:,:]))
#%% Calculate the weekly running mean average of the EKE
EKEmean=pd.DataFrame({'EKE':azoresEKE})
EKEmean=EKEmean.rolling(7,win_type=None).mean()
#%% Cool, now I want to have a plot that has a time axis from 2012 - 2018 and lines
# indicating the normal and special events
axeslabelsize=14
textsize=12

years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
days= mdates.DayLocator()
yearsFmt = mdates.DateFormatter('%Y')
empty= mdates.DateFormatter('')
fig=plt.figure(figsize=(10*1.5,8*1.5))
ax1 = fig.add_subplot(111)
#ax1.semilogy(azoresEKEtime,azoresEKE,'silver',label='Average EKE Azores')
ax1.plot(azoresEKEtime,100*EKEmean,'k',label='EKE 7-Day Running Average',linewidth=2)
for i in range(len(normEvDates)):
    ax1.axvspan(normEvDates[i],normEvDates[i], alpha=0.5, color='blue',
                label='Non-Pellet Events')

for i in range(len(specEvDates)):
    ax1.axvspan(specEvDates[i],specEvDates[i], alpha=0.5, color='red',
                label='Pellet Events')


#formatting!
ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(yearsFmt)
ax1.xaxis.set_minor_locator(months)

datemin = datetime(2012, 1, 1,0,0)
datemax = datetime(2019, 1, 1,0,0)
ax1.set_ylabel(r'EKE ($\times 10^{-2}$ m$^2$ s$^{-1}$)',fontsize=axeslabelsize)
ax1.set_ylim([0,4])
ax1.set_xlim(datemin, datemax)
ax1.tick_params(labelsize=textsize)
#ax1.set_xlabel('Time (yr)',fontsize=axeslabelsize)
ax1.set_title('Average EKE in the Azores with Non-Pellet and Pellet Events',fontsize=axeslabelsize,fontweight='bold')
ax1.tick_params(which='major',length=7)
ax1.tick_params(which='minor',length=3)            
ax1.legend(fontsize=axeslabelsize,loc=1)
fig.autofmt_xdate()
plt.tight_layout()
plt.savefig('D:\Desktop\Bern Projects\Azores Microplastic Origin\Figures/AzoresEKE_events2012-2018.jpg')


#%% Keeping it just to 2017, which are the events we are properly considering

axeslabelsize=14
textsize=12

years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
days= mdates.DayLocator()
#yearsFmt = mdates.DateFormatter('%Y')
monthsFmt=mdates.DateFormatter('%m-%Y')
fig=plt.figure(figsize=(10*1.5,8*1.5))
ax1 = fig.add_subplot(111)
#ax1.semilogy(azoresEKEtime,azoresEKE,'silver',label='Average EKE Azores')
ax1.plot(azoresEKEtime,100*EKEmean,'k',label='EKE 7-Day Running Average',linewidth=2)
for i in range(len(normEvDates)):
    ax1.axvspan(normEvDates[i],normEvDates[i], alpha=0.5, color='blue',
                label='Non-Pellet Events')

for i in range(len(specEvDates)):
    ax1.axvspan(specEvDates[i],specEvDates[i], alpha=0.5, color='red',
                label='Pellet Events')


#formatting!
ax1.xaxis.set_major_locator(months)
ax1.xaxis.set_major_formatter(monthsFmt)
ax1.xaxis.set_minor_locator(days)

datemin = datetime(2017, 1, 1,0,0)
datemax = datetime(2018, 8, 1,0,0)
ax1.set_ylabel(r'EKE ($\times 10^{-2}$ m$^2$ s$^{-1}$)',fontsize=axeslabelsize)
ax1.set_ylim([0,3])
ax1.set_xlim(datemin, datemax)
ax1.tick_params(labelsize=textsize)
#ax1.set_xlabel('Time (yr)',fontsize=axeslabelsize)
ax1.set_title('Average EKE in Azores with Non-Pellet and Pellet Events',fontsize=axeslabelsize,fontweight='bold')
ax1.tick_params(which='major',length=7)
ax1.tick_params(which='minor',length=3)            
ax1.legend(fontsize=axeslabelsize,loc=2)
fig.autofmt_xdate()
plt.tight_layout()
plt.savefig('D:\Desktop\Bern Projects\Azores Microplastic Origin\Figures/AzoresEKE_events2017-2018.jpg')

