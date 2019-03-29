# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 09:53:02 2018

@author: mrCle
I want to see where particles starting from the Azores end up based on the month
in which the particles were released
We'll combine runs for 2017-2013, for a total of 40,095 particles
"""
from netCDF4 import Dataset
from parcels import plotTrajectoriesFile,ParticleSet,JITParticle,FieldSet
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
from matplotlib import colors as c
from datetime import datetime, timedelta
from matplotlib.patches import Polygon
from copy import deepcopy
def draw_screen_poly( lats, lons, m,color):
    x, y = m( lons, lats )
    xy = zip(x,y)
    poly = Polygon( xy, edgecolor=color, linewidth=1.5,facecolor='none',zorder=300 )
    plt.gca().add_patch(poly)

#%%
File=['D:\Desktop\Bern Projects\Azores Microplastic Origin\OutputFiles/seasonality/Azores2013Season.nc',
      'D:\Desktop\Bern Projects\Azores Microplastic Origin\OutputFiles/seasonality/Azores2014Season.nc',
      'D:\Desktop\Bern Projects\Azores Microplastic Origin\OutputFiles/seasonality/Azores2015Season.nc',
      'D:\Desktop\Bern Projects\Azores Microplastic Origin\OutputFiles/seasonality/Azores2016Season.nc',
      'D:\Desktop\Bern Projects\Azores Microplastic Origin\OutputFiles/seasonality/Azores2017Season.nc']
m=0 #0 = just total, 1= total + stokes

for m in range(len(File)):
    dataset=Dataset(File[m])
    if m==0:
        time=dataset.variables['time'][:]
        lat=dataset.variables['lat'][:]
        lon=dataset.variables['lon'][:]
    else:
        lat=np.dstack((lat,dataset.variables['lat'][:]))
        lon=np.dstack((lon,dataset.variables['lon'][:]))
        time=np.dstack((time,dataset.variables['time'][:]))
    lon[lon>180]-=360
#%%
start_months=np.zeros(lon.shape)
all_times=np.zeros(lon.shape[1:])
for m in range(lon.shape[2]):
    start_times=np.sort(list(set(time[:,0,m])))
    for i in range(lon.shape[0]):
        #0=Januari, 12=december
        start_months[i,:,m]=(np.where(start_times==time[i,0,m])[0][0]-1)%12
    #Now we want the last time step
    all_times[:,m]=np.sort(list(set(time[:,:,m][~np.isnan(time[:,:,m])])))
#    all_times[:,m]=np.sort(list(set(time[:,:,m][time[:,:,m].mask==False])))
#%% Now we create the figure
latmin,latmax=-30,90
lonmin,lonmax=-101,20
plt.figure(figsize=(10*1.2,8*1.2))
my_map = Basemap(projection='cyl', llcrnrlon=lonmin, 
                  urcrnrlon=lonmax,llcrnrlat=latmin,urcrnrlat=latmax, 
                  resolution='i')
#my_map.drawcoastlines()
my_map.fillcontinents(color = 'gray')
my_map.drawmapboundary()
my_map.drawmeridians(np.arange(0, 360, 30),labels=[0,0,0,1],fontsize=12)
my_map.drawparallels(np.arange(-90, 90, 30),labels=[1,0,0,0],fontsize=12)
Title='Plastic Origin In the Azores'
plt.title(Title, fontsize=16,weight='bold')
plt.tight_layout()
#Now we draw a rectangle around the original release area
latA=[36.5,36.5,40,40,36.5]
lonA=[-31.5,-24.5,-24.5,-31.5,-31.5]
draw_screen_poly( latA, lonA, my_map,'black')
#Now we plot the final positions of all the particles after 10 years of advection
for k in range(lat.shape[-1]):
    my_map.scatter(lon[:,:,k][time[:,:,k]==all_times[0,k]],lat[:,:,k][time[:,:,k]==all_times[0,k]],
                   c=start_months[:,0,k],cmap='inferno',zorder=10,
                   vmin=0,vmax=11,s=10)
cbar=plt.colorbar(ticks=range(0,12))
cbar.ax.set_yticklabels(['January', 'February', 'March','April','May','June',
                         'July','August','September','October','November','December'],size=12)
cbar.ax.set_ylabel('Azores Arrival Month',size=14)
plt.tight_layout()
plt.savefig('D:\Desktop\Bern Projects\Azores Microplastic Origin\Figures/AzoresOriginSeason.jpg')

#%%Lets now show different seasons in seperate subplots, since it is a bit messy in the previous plot
#color=['royalblue','lawngreen','darkgreen','darkorange']
color=['red','red','red','red']
subtitle=['DJF','MAM','JJA','SON']
season=[[11,0,1],
        [2,3,4],
        [5,6,7],
        [8,9,10]]
latmin,latmax=-30,90
lonmin,lonmax=-101,20
fig=plt.figure(figsize=(10*1.2,8*1.2))
for j in range(4):
    fig.add_subplot(2,2,j+1)
    my_map = Basemap(projection='cyl', llcrnrlon=lonmin, 
                      urcrnrlon=lonmax,llcrnrlat=latmin,urcrnrlat=latmax, 
                      resolution='c')
    my_map.fillcontinents(color = 'gray')
    my_map.drawmeridians(np.arange(0, 360, 30),labels=[0,0,0,1],fontsize=11)
    my_map.drawparallels(np.arange(-90, 90, 30),labels=[1,0,0,0],fontsize=11)
#    my_map.drawcoastlines(zorder=10)
    latA=[36.5,36.5,40,40,36.5]
    lonA=[-31.5,-24.5,-24.5,-31.5,-31.5]
    draw_screen_poly( latA, lonA, my_map,'black')
    for k in range(lat.shape[-1]):
        lati=deepcopy(lat[:,:,k])
        lati[(start_months[:,:,k]!=season[j][0]) & (start_months[:,:,k]!=season[j][1]) \
             & (start_months[:,:,k]!=season[j][2])]=np.nan
        longi=deepcopy(lon[:,:,k])
        longi[(start_months[:,:,k]!=season[j][0]) & (start_months[:,:,k]!=season[j][1]) \
             & (start_months[:,:,k]!=season[j][2])]
        lati=lati[:,:][time[:,:,k]==all_times[0,k]]
        longi=longi[:,:][time[:,:,k]==all_times[0,k]]
        my_map.plot(longi,lati,'.',color=color[j],zorder=10,alpha=0.01)
    plt.title(subtitle[j])
plt.tight_layout(w_pad=5)
fig.subplots_adjust(top=0.88)
plt.suptitle('Plastic Origin in the Azores',fontweight='bold',fontsize=16)
plt.savefig('D:\Desktop\Bern Projects\Azores Microplastic Origin\Figures/AzoresOriginSeasonSubplots.jpg')
