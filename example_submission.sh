#/bin/sh
# SGE: the job name
#$ -N Azores2013
#
# The requested run-time, expressed as (xxxx sec or hh:mm:ss)
# -l h_rt=200:00:00
#
# SGE: your Email here, for job notification
#$ -M onink@climate.unibe.ch
#
# SGE: when do you want to be notified (b : begin, e : end, s : error)?
#$ -m b -m e -m s
# SGE: ouput in the current working dir
#$ -cwd
# Write Standard output and standard error to a single file
#$ -j y
#Specify that it has to go to long or short queue
#$ -q big.q
source /home/onink/.bash_profile
source /alphadata04/onink/anaconda2/bin/activate py2_parcels
cd "/alphadata04/onink/lagrangian_sim/Azores/Codes/Seasonality"
python AzoresTotalOrigin2013.py -p 10 -v
