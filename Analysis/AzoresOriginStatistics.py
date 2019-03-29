# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 14:40:42 2018

@author: mrCle
Can we identify how many particles from the Azores originate in different regions?
Yes we can!
"""
from netCDF4 import Dataset
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.path import Path
from copy import deepcopy
from collections import Counter

def draw_screen_poly( lats, lons, m,color):
    x, y = m( lons, lats )
    xy = zip(x,y)
    poly = Polygon( xy, edgecolor=color, linewidth=1.5,facecolor='none',zorder=300 )
    plt.gca().add_patch(poly)
    
def inside_polygon(vertices, point):
  """Checks if a point is inside a polygon
  
  Arguments:
    vertices (nx2 array): vertices of the polygon
    point (2 array or dx2 array): coordinates of the point
    
  Returns:
    bool: True if point is inside the polygon
  """
  
  p = Path(vertices);
  if point.ndim == 1:
    return p.contains_point(point);
  else:
    return p.contains_points(point); 
#%%
File=['D:\Desktop\Bern Projects\Azores Microplastic Origin\OutputFiles/seasonality/Azores2013Season.nc',
      'D:\Desktop\Bern Projects\Azores Microplastic Origin\OutputFiles/seasonality/Azores2014Season.nc',
      'D:\Desktop\Bern Projects\Azores Microplastic Origin\OutputFiles/seasonality/Azores2015Season.nc',
      'D:\Desktop\Bern Projects\Azores Microplastic Origin\OutputFiles/seasonality/Azores2016Season.nc',
      'D:\Desktop\Bern Projects\Azores Microplastic Origin\OutputFiles/seasonality/Azores2017Season.nc']
for m in range(len(File)):
    dataset=Dataset(File[m])
    if m==0:
        timeM=dataset.variables['time'][:,:3648]
        lat=dataset.variables['lat'][:,:3648]
        lon=dataset.variables['lon'][:,:3648]
        age=dataset.variables['Age'][:,:3648]
        distance=dataset.variables['distance'][:,:3648]
    else:
        timeM=np.vstack((timeM,dataset.variables['time'][:,:3648]))
        lat=np.vstack((lat,dataset.variables['lat'][:,:3648]))
        lon=np.vstack((lon,dataset.variables['lon'][:,:3648]))
        age=np.vstack((age,dataset.variables['Age'][:,:3648]))
        distance=np.vstack((distance,dataset.variables['distance'][:,:3648]))
lon[lon>180]-=360
time=np.unique(np.array(timeM)[~np.isnan(np.array(timeM))])
#%%
"""
We are going to create an array that identifies if a particle is beached, so 
when both the latitude and longitude are unchanged for three consecutive time steps
1=beached, 0=free
This does bring an issue for particles that are stuck in the Labrador Sea and 
Baffin Bay due to sea ice, but based on the animation these largely remain within
these basins
"""
beach=np.zeros((lon.shape))
for i in range(beach.shape[0]):
    for j in range(beach.shape[1]-3):
        if lon[i,j]==lon[i,j+1] and lon[i,j]==lon[i,j+2] and lon[i,j]==lon[i,j+3]:
            if lat[i,j]==lat[i,j+1] and lat[i,j]==lat[i,j+2] and lon[i,j]==lon[i,j+3]:
                beach[i,j:]=1
                break
#%% Now the first beached position
beach_indx=np.zeros(beach.shape[0],dtype=int)
for k in range(beach.shape[0]):
    if len(np.where(beach[k,:]==1)[0])>0:
        beach_indx[k]=np.min(np.where(beach[k,:]==1)[0])
    else:
        beach_indx[k]=9999 #indicates a particle that never beaches
#Now keep only the particles which beach at some point
lon_s=lon[np.where(beach_indx<9999)[0],:]
lat_s=lat[np.where(beach_indx<9999)[0],:]
age_s=age[np.where(beach_indx<9999)[0],:]
distance_s=distance[np.where(beach_indx<9999)[0],:]
beach_indx=beach_indx[np.where(beach_indx<9999)[0]]
#%%
latmin,latmax=-30,90
lonmin,lonmax=-101,20
plt.figure(figsize=(10*2,8*2))
my_map = Basemap(projection='cyl', llcrnrlon=lonmin, 
                  urcrnrlon=lonmax,llcrnrlat=latmin,urcrnrlat=latmax, 
                  resolution='i')
#my_map.drawcoastlines()
my_map.fillcontinents(color = 'gray')
my_map.drawmapboundary()
my_map.drawmeridians(np.arange(0, 360, 30),labels=[0,0,0,1],fontsize=16)
my_map.drawparallels(np.arange(-90, 90, 30),labels=[1,0,0,0],fontsize=16)
Title='Azores Particle Origins'
plt.title(Title, fontsize=18,weight='bold')
plt.scatter(lon_s[np.arange(lon_s.shape[0]),beach_indx],
                  lat_s[np.arange(lon_s.shape[0]),beach_indx],
                  s=5,zorder=10,c='red')
#Now comes the fun of defining the different origin regions
regionLat=[[35,35,59,59,35],#europe
           [0,0,35,35,0],#northwestern africa
           [10,10,-30,-30,10],#southwestern africa
           [-5,-5,15,15,-5],#south america
           [7,7,32,32,25.5,25.5,15,15,7],#Middle America & Carribean
           [25.5,32,45,45,25.5,25.5],#US East Coast
           [43,45,45,59,59,43,43],#Canada
           [59,59,90,90,59],#arctic
           ]
regionLon=[[-15,20,20,-15,-15],#europe
           [-20,0,0,-20,-20],#northwestern africa
           [0,20,20,0,0],#southwestern africa
           [-40,-76,-76,-40,-40],#south america
           [-76,-100,-100,-83,-80,-65,-65,-76,-76],#Middle America and Carribean
           [-80,-83,-83,-67,-67,-80],#US East Coast
           [-67,-67,-70,-70,-50,-50,-67],#Canada
           [-180,180,180,-180,-180],#arctic
           ]
#Now the labels for the different regions
reg_label=['1','2','3','4','5','6','7','8']
lonText=[-14,-19,1,-43,-96,-69.5,-54,-30]
latText=[56,32,7,12,26,41,56,60]
for z in range(len(regionLat)):
    draw_screen_poly(regionLat[z],regionLon[z], my_map,'k')
    plt.text(lonText[z],latText[z],reg_label[z],fontsize=16,weight='bold')
#Mark Faial on the map
lonF = -28.6965
latF = 38.5913
x,y = my_map(lonF, latF)
my_map.plot(x, y, '*',color='red', markersize=16)
plt.tight_layout(pad=5)
plt.savefig('D:\Desktop\Bern Projects\Azores Microplastic Origin\Figures/AzoresOriginRegions.jpg')

#%%
"""
Now we want to know how many particles in each region, average distance traveled
by particles to get to that region, and average time it takes to reach the Azores
from that region
1=Europe, 2=Northwestern Africa, 3=Southwestern Africa, 4=South America,
5=Carribean, 6= US Eastern Coast, 7=Canada, 8=Arctic
"""
origin_reg=np.zeros(len(beach_indx))
for bb in range(len(origin_reg)):
    lon_par=lon_s[bb,beach_indx[bb]]
    lat_par=lat_s[bb,beach_indx[bb]]
    for k in range(1,len(regionLon)+1):
        point=np.array((lat_par,lon_par))
        vertices=np.hstack((np.array([deepcopy(regionLat[k-1])]).T,np.array([deepcopy(regionLon[k-1])]).T))
        if inside_polygon(vertices, point)==True:
            origin_reg[bb]=k
            break
#%%
occurences=Counter(origin_reg)
#For each region the average travel distance
avg_distance=np.zeros(8)
std_distance=np.zeros(8)
for reg in range(1,9):
    avg_distance[reg-1]=np.nanmean(distance_s[np.arange(lon_s.shape[0]),beach_indx][origin_reg==reg])
    std_distance[reg-1]=np.nanstd(distance_s[np.arange(lon_s.shape[0]),beach_indx][origin_reg==reg])
#For each region the average travel time
avg_time=np.zeros(8)
std_time=np.zeros(8)
for reg in range(1,9):
    avg_time[reg-1]=np.nanmean(age_s[np.arange(lon_s.shape[0]),beach_indx][origin_reg==reg])/365 #in years
    std_time[reg-1]=np.nanstd(age_s[np.arange(lon_s.shape[0]),beach_indx][origin_reg==reg])/365 #in years


#%% Now we want to plot the longest distance travelled
max_dist=np.unique(distance_s[np.arange(lon_s.shape[0]),beach_indx])
latmin,latmax=-30,90
lonmin,lonmax=-101,20
plt.figure(figsize=(10*2,8*2))
my_map = Basemap(projection='cyl', llcrnrlon=lonmin, 
                  urcrnrlon=lonmax,llcrnrlat=latmin,urcrnrlat=latmax, 
                  resolution='i')
#my_map.drawcoastlines()
my_map.fillcontinents(color = 'gray')
my_map.drawmapboundary()
my_map.drawmeridians(np.arange(0, 360, 30),labels=[0,0,0,1],fontsize=16)
my_map.drawparallels(np.arange(-90, 90, 30),labels=[1,0,0,0],fontsize=16)
Title='Longest Trajectories'
plt.title(Title, fontsize=18,weight='bold')
plt.plot(lon_s[np.where(distance_s==max_dist[-1])[0][0],:],lat_s[np.where(distance_s==max_dist[-1])[0][0],:], 
               label='1st, Distance= '+str(int(max_dist[-1]))+'km',c='gold')
plt.plot(lon_s[np.where(distance_s==max_dist[-2])[0][0],:],lat_s[np.where(distance_s==max_dist[-2])[0][0],:], 
               label='2nd, Distance= '+str(int(max_dist[-2]))+'km',c='silver')
plt.plot(lon_s[np.where(distance_s==max_dist[-3])[0][0],:],lat_s[np.where(distance_s==max_dist[-3])[0][0],:], 
               label='3rd, Distance= '+str(int(max_dist[-3]))+'km',c='peru')
plt.legend()
lonF = -28.6965
latF = 38.5913
x,y = my_map(lonF, latF)
my_map.plot(x, y, '*',color='red', markersize=16)
plt.tight_layout(pad=5)
plt.savefig('D:\Desktop\Bern Projects\Azores Microplastic Origin\Figures/AzoresFurthestTravelers.jpg')

#%% I want to plot the 21 trajectories that originate from Europe
euro=np.where(origin_reg==1)[0]
latmin,latmax=-30,90
lonmin,lonmax=-101,20
plt.figure(figsize=(10*2,8*2))
my_map = Basemap(projection='cyl', llcrnrlon=lonmin, 
                  urcrnrlon=lonmax,llcrnrlat=latmin,urcrnrlat=latmax, 
                  resolution='i')
#my_map.drawcoastlines()
my_map.fillcontinents(color = 'gray')
my_map.drawmapboundary()
my_map.drawmeridians(np.arange(0, 360, 30),labels=[0,0,0,1],fontsize=16)
my_map.drawparallels(np.arange(-90, 90, 30),labels=[1,0,0,0],fontsize=16)
Title='Trajectories from Europe'
plt.title(Title, fontsize=18,weight='bold')
for ll in range(len(euro)):
    plt.plot(lon_s[euro[ll],:beach_indx[euro[ll]]],lat_s[euro[ll],:beach_indx[euro[ll]]],
             c='blue',alpha=0.3)
lonF = -28.6965
latF = 38.5913
x,y = my_map(lonF, latF)
my_map.plot(x, y, '*',color='red', markersize=16)
plt.tight_layout(pad=5)
plt.savefig('D:\Desktop\Bern Projects\Azores Microplastic Origin\Figures/AzoresFromEurope.jpg')
