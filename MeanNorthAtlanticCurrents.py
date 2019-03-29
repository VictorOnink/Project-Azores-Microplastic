# -*- coding: utf-8 -*-
"""
Created on Fri Nov 02 11:51:46 2018

@author: mrCle
Mean Atlantic Currents

"""
from netCDF4 import Dataset
import numpy as np
from matplotlib import colors
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.ticker import LogFormatter


def draw_screen_poly( lats, lons, m,color):
    x, y = m( lons, lats )
    xy = zip(x,y)
    poly = Polygon( xy, edgecolor=color, linewidth=1.5,facecolor='none',zorder=300 )
    plt.gca().add_patch(poly)
#%%
fileTot='D:\Desktop\Thesis\ParcelsFigData\Data\Global\OutputFiles\Onink et al/AverageTotalCurrents.nc'
datasetTot=Dataset(fileTot)
latTot=datasetTot.variables['latitude'][:]
lonTot=datasetTot.variables['longitude'][:]
lonTot[lonTot>180]-=360
uTot=datasetTot.variables['Uavg'][:]
vTot=datasetTot.variables['Vavg'][:]
magTot=np.sqrt(np.square(uTot)+np.square(vTot))
magTot[magTot==0]=np.nan

def plotDensity(typ,lon,lat,u,v,mag):
    Lon,Lat=np.meshgrid(lon,lat)
    latmin,latmax=-30,90
    lonmin,lonmax=-101,20
    my_map = Basemap(projection='cyl', llcrnrlon=lonmin, 
                      urcrnrlon=lonmax,llcrnrlat=latmin,urcrnrlat=latmax, 
                      resolution='i')
    my_map.fillcontinents(color = 'gray',zorder=20)
    my_map.drawmapboundary()
    my_map.drawmeridians(np.arange(0, 360, 30),labels=[0,0,0,1],fontsize=16)
    if (typ+1)%2==1:
        my_map.drawparallels(np.arange(-90, 91, 30),labels=[1,0,0,0],fontsize=16)
    else:
        my_map.drawparallels(np.arange(-90, 91, 30),fontsize=16)
    normU,normV=np.divide(u,mag),np.divide(v,mag)
    if typ!=3:
        step=10
    else:
        step=1
    plt.quiver(Lon[::step,::step],Lat[::step,::step],normU[::step,::step],normV[::step,::step],
                      width=2e-3,color='k',zorder=5,scale=10, scale_units='inches')
    size=plt.pcolormesh(Lon,Lat,mag,zorder=1,cmap='rainbow',
                        norm=colors.LogNorm(1e-2,1))
#                        vmin=0,vmax=.6)
    title=['Mean Currents','(b) Ekman Currents','(c) Geostrophic Currents','(d) Stokes Drift']
    plt.title(title[typ],fontsize=18,fontweight='bold')
    lonF = -28.6965
    latF = 38.5913
    x,y = my_map(lonF, latF)
    my_map.plot(x, y, '*',color='r', markersize=16)
    return size
fig,axes=plt.subplots(nrows=1, ncols=1,figsize=(10*1.2,8*1.2))
plt.subplot(1,1,1)
size=plotDensity(0,lonTot,latTot,uTot[0,:,:],vTot[0,:,:],magTot[0,:,:])
fig.subplots_adjust(right=0.9)
cbar_ax = fig.add_axes([0.88, 0.08, 0.02, 0.82])
formatter = LogFormatter(10, labelOnlyBase=True) 
cbar=fig.colorbar(size,cax=cbar_ax)
cbar.ax.tick_params(labelsize=16)
labels=['<0.01','0.1','1<']
#labelsM=["%.2f" % z for z in labels]
actualLabels=[]
k=0
for i in range(20):
    if i%9==0:
        actualLabels.append(labels[k])
        k+=1
    else:
        actualLabels.append('')
cbar.ax.set_yticklabels(actualLabels)
cbar.set_label("Mean Current Velocity (m s$^{-1}$)", rotation=90,fontsize=16)
plt.tight_layout(pad=5)
plt.savefig('D:\Desktop\Bern Projects\Azores Microplastic Origin\Figures/MeanNorthAtlanticCurrentsMICRO.jpg')

