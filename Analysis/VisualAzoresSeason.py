# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 10:08:27 2018

@author: Mayer
Animation for the seasonality study
"""
from netCDF4 import Dataset
from parcels import plotTrajectoriesFile,ParticleSet,JITParticle,FieldSet
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
from datetime import datetime, timedelta
from matplotlib.patches import Polygon
def draw_screen_poly( lats, lons, m,color):
    x, y = m( lons, lats )
    xy = zip(x,y)
    poly = Polygon( xy, edgecolor=color, linewidth=1.5,facecolor='none',zorder=300 )
    plt.gca().add_patch(poly)

#%%
#lon=np.load('D:\Desktop\Thesis\ParcelsFigData\Data\North Pacific\InputArray/LonsEastTestgrid0_3.npy')
#lat=np.load('D:\Desktop\Thesis\ParcelsFigData\Data\North Pacific\InputArray/LatsWestTestgrid0_3.npy')
#filenames = {'U': "D:\Desktop\Thesis\Data sets\GlobCurrent/2005/AllTogether/20050101*.nc",
#             'V': "D:\Desktop\Thesis\Data sets\GlobCurrent/2005/AllTogether/20050101*.nc"}
#variables = {'U': 'eastward_eulerian_current_velocity',
#             'V': 'northward_eulerian_current_velocity'}
#dimensions = {'lat': 'lat',
#              'lon': 'lon',
#              'time': 'time'}
#fieldset = FieldSet.from_netcdf(filenames, variables, dimensions,allow_time_extrapolation=True)

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
    else:
        timeM=np.vstack((timeM,dataset.variables['time'][:,:3648]))
        lat=np.vstack((lat,dataset.variables['lat'][:,:3648]))
        lon=np.vstack((lon,dataset.variables['lon'][:,:3648]))
lon[lon>180]-=360        
time=np.sort(np.unique(np.array(timeM)[~np.isnan(np.array(timeM))]))
#%%
latmin,latmax=-30,90
lonmin,lonmax=-101,20
plt.figure(figsize=(10*1.5,8*1.5))
my_map = Basemap(projection='cyl', llcrnrlon=lonmin, 
                  urcrnrlon=lonmax,llcrnrlat=latmin,urcrnrlat=latmax, 
                  resolution='l')
#my_map.drawcoastlines()
my_map.fillcontinents(color = 'gray')
my_map.drawmapboundary()
#my_map.drawmeridians(np.arange(0, 360, 30))
#my_map.drawparallels(np.arange(-90, 90, 30))
Title='Azores Plastic Origins'
plt.title(Title, fontsize=14,weight='bold')
plt.tight_layout()
#Now we draw a rectangle around the original release area
latA=[36.5,36.5,40,40,36.5]
lonA=[-31.5,-24.5,-24.5,-31.5,-31.5]
draw_screen_poly( latA, lonA, my_map,'black')
#text=plt.annotate('hi', xy=(0.5, 0.9), xycoords='axes fraction')
text=plt.text(-98.75, -27.1,'',
                     ha='center',va='center',fontsize=12,
                     bbox={'facecolor':'white', 'alpha':1,'pad':10},zorder=200,
                     horizontalalignment='left')
x,y = my_map(0, 0)
point = my_map.plot(x, y, 'r.', markersize=5,zorder=1)[0]
def init():
    point.set_data([], [])
    point.set_zorder(0)
    text.set_text('')
    return point,#,text

# animation function.  This is called sequentially
def animate(i):
    lons, lats = lon[timeM==time[-1-3*i]] , lat[timeM==time[-1-3*i]]
    Time=datetime(2000,1,1)+timedelta(seconds=time[-1-3*i])
    x, y = my_map(lons, lats)
    point.set_data(x, y)
    point.set_zorder(0)
    text.set_text('Date='+Time.strftime('%d-%m-%y'))
#    text.set_text('Date='+Time.strftime('%m-%Y'))
    return point,text
# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(plt.gcf(), animate, init_func=init,
                               frames=len(time)/3, interval=10, blit=True)
anim.save('D:\Desktop\Bern Projects\Azores Microplastic Origin/Animations/AzoresOrigin2017_2013.mov', 
          fps=30)
#extra_args=['-vcodec', 'libx264']
#plt.show()
