# -*- coding: utf-8 -*-
"""
Created on Wed Apr 03 14:02:03 2019

@author: mrCle
So the plots don't really give a clear answer one way or another with regards to 
whether there is a link between EKE and the events, so we'll try to add some 
statistics to the mix
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
from scipy.stats import pointbiserialr


earth_radius = 6371.0 #km
degrees_to_radians = math.pi/180.0
radians_to_degrees = 180.0/math.pi

def change_in_latitude(km):
    "Given a distance north, return the change in latitude."
    return (km/earth_radius)*radians_to_degrees

#%% First, I need to have all the non-event days
excel='D:\Desktop\Bern Projects\Azores Microplastic Origin/2019_CPieper_non-event_days.xlsx'
FileEx=pd.read_excel(excel)
normEv=FileEx['Date dd/mm/yy'].astype('|S')
normEvDates=[]
for i in range(len(normEv)):
    date=datetime.strptime(normEv[i],'%Y-%m-%d')
    date=date.replace(minute=0)
    normEvDates.append(date)

# Now I will divide the individual days into coherent events, where I consider
# all measurements within a week of each other as a single event, as following
# Erik's sorting criteria. The date of the events is the first day on which
# measurements were taken.
normEvents=[]
for i in range(len(normEvDates)):
    if i==0:
        normEvents.append(normEvDates[i])
        eventstart=normEvDates[i]
    else:
        if (normEvDates[i]-eventstart).days>9:
            normEvents.append(normEvDates[i])
            eventstart=normEvDates[i]
     
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

# Same sorting into events as with the normal days
specEvents=[]
for i in range(len(specEvDates)):
    if i==0:
        specEvents.append(specEvDates[i])
        eventstart=specEvDates[i]
    else:
        if (specEvDates[i]-eventstart).days>9:
            specEvents.append(specEvDates[i])
            eventstart=specEvDates[i]
#%%Finally, I need to get the EKE, which I should have in my files
azoresAltiEKE=[]
azoresAltiEKEtime=[]
directory='D:\Desktop\Bern Projects\Azores Microplastic Origin\EKE'
ls=os.listdir(directory)[:-1] #last one is a directory, don't want that
for File in ls:
    datasetAlti=Dataset(directory+'/'+File)
    lonAlti=datasetAlti.variables['longitude'][1313:1342]
    latAlti=datasetAlti.variables['latitude'][505:521]
    EKEalti=datasetAlti.variables['EKE'][:,505:521,1313:1342]
    timeAlti=datasetAlti.variables['time'][:]
    azoresAltiEKEtime.append(datetime(1950,1,1,0,0)+timedelta(days=timeAlti[0]))
    azoresAltiEKE.append(np.nanmean(EKEalti[0,:,:]))
azoresAltiEKE=np.array(azoresAltiEKE)

#%% Calculate the weekly running mean average of the EKE
EKEmeanAlti=pd.DataFrame({'EKE':azoresAltiEKE})
EKEmeanAlti=EKEmeanAlti.rolling(7,win_type=None).mean()
EKEmeanAlti=np.array(EKEmeanAlti)

#%% Ok, now we have events, so I want to have avg EKE between 2 weeks and present
# to each event, since of course there might be some lag between when the EKE rises 
# due to an eddy and when we actually see the plastic washed up on shore
specEKE=np.zeros((14,31))
normEKE=np.zeros((14,32))
for i in range(14):
    for k in range(len(azoresAltiEKEtime)):
        for j in range(len(normEvents)):
            if azoresAltiEKEtime[k]==(normEvents[j]-timedelta(days=i)):
                normEKE[i,j]+=EKEmeanAlti[k,0]
        for j in range(len(specEvents)):
            if azoresAltiEKEtime[k]==(specEvents[j]-timedelta(days=i)): 
                specEKE[i,j]+=EKEmeanAlti[k,0]
meanEKEspec=np.mean(specEKE,axis=1)
meanEKEnorm=np.mean(normEKE,axis=1)
stdEKEspec=np.std(specEKE,axis=1)
stdEKEnorm=np.std(normEKE,axis=1)
#%% Now the first thing I want to do is see how the average EKE compares for the
# normal and special events with the different lags built in.

fig,ax=plt.subplots(figsize=(20,16))
bar_width,opacity = 0.35,0.4
lag=np.arange(14)

rects1 = ax.bar(lag, meanEKEnorm, bar_width,
                alpha=opacity, color='b',
                yerr=stdEKEnorm,
                label='Non-Pellet Events')

rects2 = ax.bar(lag + bar_width, meanEKEspec, bar_width,
                alpha=opacity, color='r',
                yerr=stdEKEspec,
                label='Pellet Events')
plt.legend()
plt.xlabel('time prior to events (days)')
plt.ylabel('EKE')

#%% I want to plot the mean with each of the actual measurements too, see if we
# get anything from this

fig,ax=plt.subplots(figsize=(20,16))
bar_width=0.35

plt.plot(lag,meanEKEnorm,'o',markeredgecolor='k',markersize=8,
         color='blue',label='Non-Pellet Events')
plt.plot(lag,normEKE,'o',alpha=0.3,markersize=5,
         color='blue')
plt.plot(lag+bar_width,meanEKEspec,'o',markeredgecolor='k',markersize=8,
         color='red',label='Pellet Events')
plt.plot(lag+bar_width,specEKE,'o',alpha=0.3,markersize=5,
         color='red')

plt.legend()
plt.xlabel('time prior to events (days)')
plt.ylabel('EKE')

#%% Now there has to be some form of correlation we can try, although based on
# the earlier plots I doubt it'll be anything significant
allEKE=np.hstack((specEKE,normEKE))
allEvents=np.hstack((np.ones(specEKE.shape[1]),np.zeros(normEKE.shape[1])))
corrEventsLags=np.zeros((14,2))

for i in range(14):
    corrEventsLags[i,0],corrEventsLags[i,1]=pointbiserialr(allEvents,allEKE[i,:])
# as expected, nothing significant. Will need to wait for Ana to have a better idea
# of what to try, since this clearly isn't the way
