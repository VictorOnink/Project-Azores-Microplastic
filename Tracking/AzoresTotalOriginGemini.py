# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 14:43:49 2018

@author: Tori Amos
"""

from parcels import FieldSet, ParticleSet, JITParticle, AdvectionRK4,ErrorCode, plotTrajectoriesFile,Variable
from datetime import timedelta, datetime
import numpy as np
from operator import attrgetter
import math
#We can add or remove all the zeros according to preference. In case that they are left there, we only get daily data for the currents which will end up with the code running faster, but we do lose time resolution. Tests will determine if this loss in time resolution is actually important
filenames = {'U': "/scratch/Victor/TotalData/20*.nc",
             'V': "/scratch/Victor/TotalData/20*.nc"}
variables = {'U': 'eastward_eulerian_current_velocity',
             'V': 'northward_eulerian_current_velocity'}
dimensions = {'lat': 'lat',
              'lon': 'lon',
              'time': 'time'}
#%%
#Create the fieldset with the periodic halo and time extrapolation for the EKE
print 'Creating the fieldset'
fieldset = FieldSet.from_netcdf(filenames, variables, dimensions,allow_time_extrapolation=True)
#fieldset.add_periodic_halo(zonal=True)

#The starting coordinates of the Particles, for the North Pacific. They are generated
#by the code NAgrid.py, graciously send to me by David.
lons=np.load('/home/students/4056094/Desktop/Azores/InputDistribution/LatsAzoresInitialDistribution.npy')
lats=np.load('/home/students/4056094/Desktop/Azores/InputDistribution/LonsAzoresInitialDistribution.npy')
#lons, lats = np.meshgrid(lon,lat)


#And now we define what sort of particles we are actually dealing with
class SampleParticle(JITParticle):
    Age=Variable('Age',initial=0.,dtype=np.float32)#agr is gonna be in seconds
    prev_time=Variable('prev_time',initial=attrgetter('time'),to_write=False)
    #Now the part to track the distance covered
    distance = Variable('distance', initial=0., dtype=np.float32)
    prev_lon = Variable('prev_lon', dtype=np.float32, to_write=False,
                        initial=attrgetter('lon'))
    prev_lat = Variable('prev_lat', dtype=np.float32, to_write=False,
                        initial=attrgetter('lat'))

#The starting point of the similation and the endtime
print 'Creating the pset'
starttime=datetime(2014,12,31,21,0)
endtime=datetime(2002,1,1,0,0)
pset = ParticleSet(fieldset=fieldset, pclass=SampleParticle, lon=lons, lat=lats,time=starttime)
#%% All the different functions/kernels we want to have
def DeleteParticle(particle, fieldset, time, dt):
    particle.delete()
    print 'we deleted it at '+str(particle.lon)+' and '+str(particle.lat)
def AgeSample(particle, fiedset,time,dt):
    current_time=particle.time
    timedifference=abs(current_time-particle.prev_time)/86400 #get the timedifference in days
    particle.Age+=timedifference
    particle.prev_time=current_time
def TotalDistance(particle, fieldset, time, dt):
    # Calculate the distance in latitudinal direction (using 1.11e2 kilometer per degree latitude)
    lat_dist = (particle.lat - particle.prev_lat) * 1.11e2
    # Calculate the distance in longitudinal direction, using cosine(latitude) - spherical earth
    lon_dist = (particle.lon - particle.prev_lon) * 1.11e2 * math.cos(particle.lat * math.pi / 180)
    # Calculate the total Euclidean distance travelled by the particle
    particle.distance += math.sqrt(math.pow(lon_dist, 2) + math.pow(lat_dist, 2))
    particle.prev_lon = particle.lon  # Set the stored values for next iteration.
    particle.prev_lat = particle.lat
Distsam=pset.Kernel(TotalDistance) 
Agesam=pset.Kernel(AgeSample)   
totalKernal=AdvectionRK4+Distsam+Agesam
#%%
savestep=24
pfile = pset.ParticleFile(name="/scratch/Victor/AzoresOriginTotalStokes",
                          outputdt=timedelta(hours=savestep))

Time=starttime
steps=0
while Time>=endtime:
    steps+=1
    Time-=timedelta(hours=savestep)
print 'now we start advecting them for how many steps? '+str(steps)

pset.execute(totalKernal,
             runtime=timedelta(hours=savestep*(steps-1)),  # runtime controls the interval of the plots
             dt=-timedelta(minutes=30),
             recovery={ErrorCode.ErrorOutOfBounds: DeleteParticle},
             output_file=pfile
             )  # the recovery kernel
