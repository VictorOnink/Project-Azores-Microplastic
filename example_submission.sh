#/bin/sh
# SGE: the job name
#$ -N Correlations2002_2014
#
# The requested run-time, expressed as (xxxx sec or hh:mm:ss)
#$ -l h_rt=200:00:00
#
# SGE: your Email here, for job notification
#$ -M v.onink@uu.nl
#
# SGE: when do you want to be notified (b : begin, e : end, s : error)?
#$ -m b -m e -m s
# SGE: ouput in the current working dir
#$ -cwd    
#Specify which node I want the code to run in
##$ -l h=science-bs35
#Specify that it has to go to long or short queue
#$ -q long.q
source /home/students/4056094/.bash_profile
#cd "/home/students/4056094/Desktop/Thesis/ParcelsOutput/North Atlantic/Codes"
#python AtlanticWindageTracking5per.py -p 10 -v
cd "/scratch/Victor"
python globalCorrelationRegressionWindageStokesV4u_v.py
