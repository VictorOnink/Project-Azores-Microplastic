# -*- coding: utf-8 -*-
"""
Created on Tue Oct 09 13:51:20 2018

@author: mrCle

Goal here is to read in the database, and then sort through it so that we pick out
the eddies that (at some point) were within the azores

The definition of the azores area follows that of wikipedia...
24.5-31.5 W, 36.5-40.0 N

Dataset is the most recent version, so it covers 1993/01/01-2018/01/18
"""

import numpy as np
from netCDF4 import Dataset
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import geopy.distance as dis
from Circles.circles import circle
import math

earth_radius = 6371.0 #km
degrees_to_radians = math.pi/180.0
radians_to_degrees = 180.0/math.pi

def change_in_latitude(km):
    "Given a distance north, return the change in latitude."
    return (km/earth_radius)*radians_to_degrees

#%%
File='D:\Desktop\Bern Projects\Azores Microplastic Origin/eddy_trajectory_2.0exp_19930101_20180118.nc'
eddy_set=Dataset(File)
track=eddy_set.variables['track'][:]
lon=eddy_set.variables['longitude'][:]
lon[lon>180]-=360
lat=eddy_set.variables['latitude'][:]
radius=eddy_set.variables['speed_radius'][:]
time=eddy_set.variables['time'][:] #days since 1950-01-01
#%%
track_ID=[]
begin=(datetime(2017,1,1)-datetime(1950,1,1)).days
end=(datetime(2018,1,1)-datetime(1950,1,1)).days
for i in range(len(track)):
    if time[i]>begin and end>time[i]:    
        if -21.5>lon[i]>-34.5:
            if 43>lat[i]>33.5:
                track_ID.append(int(track[i]))
track_ID=np.sort(list(set(track_ID)))
#%%
#first select the colors of the tracks to have at least some consistency between figures
track_color=['orangered','limegreen','lightskyblue','c','violet']
#Now the actual figures
year=2017
month=[2,3,4,5,6,11,12]
day=[13,14,10,25,5,17,13]
fig,axes=plt.subplots(nrows=1, ncols=1,figsize=(10*1.5,7.2*1.5))
for event in range(len(month)):
    time_start=(datetime(year,month[event],day[event])-timedelta(days=25)-datetime(1950,1,1)).days
    time_end=(datetime(year,month[event],day[event])+timedelta(days=5)-datetime(1950,1,1)).days
    #%Now sort the azores eddies such that we only keep those which encompass Faial
    #at some point in the given time period
    lonFaial,latFaial = -28.6965,38.5913
    track_ID_faial=[]
    for j in range(len(track_ID)):
        lon_sub=lon[track==int(track_ID[j])]
        lat_sub=lat[track==int(track_ID[j])]
        time_sub=time[track==int(track_ID[j])]
        radius_sub=radius[track==int(track_ID[j])]
    #    print max(radius_sub)
        for z in range(len(lon_sub)):
            if time_sub[z]>time_start and time_sub[z]<time_end:
                dist=dis.vincenty((lonFaial,latFaial), (lon_sub[z],lat_sub[z])).km
                if dist<radius_sub[z]:
                    track_ID_faial.append(track_ID[j])
    track_ID_faial=np.sort(list(set(track_ID_faial)))
            
    
    #% Check if the sorting actually worked
    latmin,latmax=30,45
    lonmin,lonmax=-40,-15
    ax=plt.subplot(3,3,event+1)
    my_map = Basemap(projection='cyl', llcrnrlon=lonmin, 
                      urcrnrlon=lonmax,llcrnrlat=latmin,urcrnrlat=latmax, 
                      resolution='i')
    my_map.fillcontinents(color = 'gray')
    my_map.drawmeridians(np.arange(0, 360, 10),labels=[0,0,0,1],fontsize=11)
    my_map.drawparallels(np.arange(-90, 90, 10),labels=[1,0,0,0],fontsize=11)
    my_map.drawcoastlines(zorder=10)
    for k in range(len(track_ID_faial)):
        ind=track==track_ID_faial[k]
        my_map.plot(lon[ind],lat[ind],'-',color=track_color[k])
        
    lonF = -28.6965
    latF = 38.5913
    x,y = my_map(lonF, latF)
    my_map.plot(x, y, 'r*', markersize=12)
    ax.set_title(str(year)+'-'+str(month[event]))
plt.tight_layout(w_pad=5)
fig.subplots_adjust(top=0.88)
plt.suptitle('Faial Microplastic Events (Single Eddy Radius Sorting)',fontweight='bold',fontsize=16)
#plt.savefig('D:\Desktop\Bern Projects\Azores Microplastic Origin\Figures/EddiesEventsSingleEddyRadius.jpg')

#%%
#first select the colors of the tracks to have at least some consistency between figures
track_color=['orangered','limegreen','lightskyblue','c','violet']
#now the sorting
year=2017
month=[2,3,4,5,6,11,12]
day=[13,14,10,25,5,17,13]#day of the event, middle date if it was multiple days
fig,axes=plt.subplots(nrows=1, ncols=1,figsize=(10*1.5,7.2*1.5))
for event in range(len(month)):
    time_start=(datetime(year,month[event],day[event])-timedelta(days=25)-datetime(1950,1,1)).days
    time_end=(datetime(year,month[event],day[event])+timedelta(days=5)-datetime(1950,1,1)).days
    #%Now sort the azores eddies such that we only keep those which encompass Faial
    #at some point in the given time period
    lonFaial,latFaial = -28.6965,38.5913
    track_ID_faial=[]
    for j in range(len(track_ID)):
        lon_sub=lon[track==int(track_ID[j])]
        lat_sub=lat[track==int(track_ID[j])]
        time_sub=time[track==int(track_ID[j])]
        radius_sub=radius[track==int(track_ID[j])]
    #    print max(radius_sub)
        for z in range(len(lon_sub)):
            if time_sub[z]>time_start and time_sub[z]<time_end:
                dist=dis.vincenty((lonFaial,latFaial), (lon_sub[z],lat_sub[z])).km
                if dist<2*radius_sub[z]:
                    track_ID_faial.append(track_ID[j])
    track_ID_faial=np.sort(list(set(track_ID_faial)))
            
    
    #% Check if the sorting actually worked
    latmin,latmax=35,42
    lonmin,lonmax=-35,-23
    ax=plt.subplot(3,3,event+1)
    my_map = Basemap(projection='cyl', llcrnrlon=lonmin, 
                      urcrnrlon=lonmax,llcrnrlat=latmin,urcrnrlat=latmax, 
                      resolution='i')
    my_map.fillcontinents(color = 'gray')
    my_map.drawmeridians(np.arange(0, 360, 5),labels=[0,0,0,1],fontsize=11)
    my_map.drawparallels(np.arange(-90, 90, 5),labels=[1,0,0,0],fontsize=11)
    my_map.drawcoastlines(zorder=10)
    for k in range(len(track_ID_faial)):
        ind=track==track_ID_faial[k]
        my_map.plot(lon[ind],lat[ind],'-',color=track_color[k])
        my_map.plot(lon[ind][0],lat[ind][0],'^',color=track_color[k])
        event_day=(datetime(year,month[event],day[event])-datetime(1950,1,1)).days
        x1,y1=my_map(lon[ind][time[ind]==event_day],lat[ind][time[ind]==event_day])
        if len(x1)>0:
            x2,y2=my_map(lon[ind][time[ind]==event_day],lat[ind][time[ind]==event_day]+change_in_latitude(radius[ind][time[ind]==event_day][0]))
            circle1 = plt.Circle((x1, y1), y2-y1, color=track_color[k],fill=True,alpha=0.5)
            ax.add_artist(circle1)
        
    lonF = -28.6965
    latF = 38.5913
    x,y = my_map(lonF, latF)
    my_map.plot(x, y, '*',c='red', markersize=16,zorder=100)
    ax.set_title(str(year)+'-'+str(month[event]))
plt.tight_layout(w_pad=5,pad=5)
fig.subplots_adjust(top=0.88)
plt.suptitle('Faial Microplastic Events (Double Eddy Radius Sorting)',fontweight='bold',fontsize=16)
plt.savefig('D:\Desktop\Bern Projects\Azores Microplastic Origin\Figures/EddiesEventsDoubleEddyRadius.jpg')
#%%
event=-2
time_start=(datetime(year,month[event],13)-datetime(1950,1,1)).days
if month[event]>11:
    time_end=(datetime(year+1,1,1)-datetime(1950,1,1)).days
else:
    time_end=(datetime(year,month[event]+1,22)-datetime(1950,1,1)).days
#%Now sort the azores eddies such that we only keep those which encompass Faial
#at some point in the given time period
lonFaial,latFaial = -28.6965,38.5913
track_ID_faial=[]
for j in range(len(track_ID)):
    lon_sub=lon[track==int(track_ID[j])]
    lat_sub=lat[track==int(track_ID[j])]
    time_sub=time[track==int(track_ID[j])]
    radius_sub=radius[track==int(track_ID[j])]
#    print max(radius_sub)
    for z in range(len(lon_sub)):
        if time_sub[z]>time_start and time_sub[z]<time_end:
            dist=dis.vincenty((lonFaial,latFaial), (lon_sub[z],lat_sub[z])).km
            if dist<2*radius_sub[z]:
                track_ID_faial.append(track_ID[j])
track_ID_faial=np.sort(list(set(track_ID_faial)))
latmin,latmax=30,45
lonmin,lonmax=-40,-15
ax=plt.subplot(1,1,1)
my_map = Basemap(projection='cyl', llcrnrlon=lonmin, 
                  urcrnrlon=lonmax,llcrnrlat=latmin,urcrnrlat=latmax, 
                  resolution='i')
my_map.fillcontinents(color = 'gray')
my_map.drawmeridians(np.arange(0, 360, 10),labels=[0,0,0,1],fontsize=11)
my_map.drawparallels(np.arange(-90, 90, 10),labels=[1,0,0,0],fontsize=11)
my_map.drawcoastlines(zorder=10)
for k in range(len(track_ID_faial)):
    ind=track==track_ID_faial[k]
    my_map.plot(lon[ind],lat[ind],'-')
lonF = -28.6965
latF = 38.5913
x,y = my_map(lonF, latF)
my_map.plot(x, y, 'r*', markersize=12)
ax.set_title(str(year)+'-'+str(month[event]))

#%%
#We'll limit the sorting to all tracks since 2010
year=2017
month=[2,3,4,5,6,11,12]
day=[13,14,10,25,5,17,13]#day of the event, middle date if it was multiple days
track_color=['orangered','limegreen','lightskyblue','c','violet']

fig,axes=plt.subplots(nrows=1, ncols=1,figsize=(10*1.5,7.2*1.5))
for event in range(len(month)):
    time_start=(datetime(year,month[event],day[event])-timedelta(days=25)-datetime(1950,1,1)).days
    time_end=(datetime(year,month[event],day[event])+timedelta(days=5)-datetime(1950,1,1)).days
    #%Now sort the azores eddies such that we only keep those which encompass Faial
    #at some point in the given time period
    lonFaial,latFaial = -28.6965,38.5913
    track_ID_faial=[]
    for j in range(len(track_ID)):
        lon_sub=lon[track==int(track_ID[j])]
        lat_sub=lat[track==int(track_ID[j])]
        time_sub=time[track==int(track_ID[j])]
        radius_sub=radius[track==int(track_ID[j])]
    #    print max(radius_sub)
        for z in range(len(lon_sub)):
            if time_sub[z]>time_start and time_sub[z]<time_end:
                dist=dis.vincenty((lonFaial,latFaial), (lon_sub[z],lat_sub[z])).km
                if dist<200:
                    track_ID_faial.append(track_ID[j])
    track_ID_faial=np.sort(list(set(track_ID_faial)))
            
    
    #% Check if the sorting actually worked
    latmin,latmax=35,42
    lonmin,lonmax=-35,-23
    ax=plt.subplot(3,3,event+1)
    my_map = Basemap(projection='cyl', llcrnrlon=lonmin, 
                      urcrnrlon=lonmax,llcrnrlat=latmin,urcrnrlat=latmax, 
                      resolution='i')
    my_map.fillcontinents(color = 'gray')
    my_map.drawmeridians(np.arange(0, 360, 5),labels=[0,0,0,1],fontsize=11)
    my_map.drawparallels(np.arange(-90, 90, 5),labels=[1,0,0,0],fontsize=11)
    my_map.drawcoastlines(zorder=10)
    for k in range(len(track_ID_faial)):
        ind=track==track_ID_faial[k]
        my_map.plot(lon[ind],lat[ind],'-',color=track_color[k])
        my_map.plot(lon[ind][0],lat[ind][0],'^',color=track_color[k])
        event_day=(datetime(year,month[event],day[event])-datetime(1950,1,1)).days
        x1,y1=my_map(lon[ind][time[ind]==event_day],lat[ind][time[ind]==event_day])
        if len(x1)>0:
            x2,y2=my_map(lon[ind][time[ind]==event_day],lat[ind][time[ind]==event_day]+change_in_latitude(radius[ind][time[ind]==event_day][0]))
            circle1 = plt.Circle((x1, y1), y2-y1, color=track_color[k],fill=True,alpha=0.5)
            ax.add_artist(circle1)
    lonF = -28.6965
    latF = 38.5913
    x,y = my_map(lonF, latF)
    my_map.plot(x, y, '*',c='red', markersize=16,zorder=100)
    ax.set_title(str(year)+'-'+str(month[event]))
plt.tight_layout(w_pad=5,pad=5)
fig.subplots_adjust(top=0.88)
plt.suptitle('Faial Microplastic Events (Eddy Center <200km of Faial)',fontweight='bold',fontsize=16)
plt.savefig('D:\Desktop\Bern Projects\Azores Microplastic Origin\Figures/EddiesEvents200kmFaial.jpg')