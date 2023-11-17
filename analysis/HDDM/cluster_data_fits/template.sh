#!/bin/bash -login

## walltime HH:MM:SS
#SBATCH -t 168:00:00

## nodes
#SBATCH --cpus-per-task=1

## mem
#SBATCH --mem-per-cpu=15G

## name of job
#SBATCH --job-name=__JOBNAME__

## email notification
#SBATCH --mail-user=seandamiandevine@gmail.com
#SBATCH --mail-type=__MAILTYPE__

## save SLURM output to specified directory
#SBATCH --output=__OUTPATH__logs/__JOBNAME__.out  

## load relevant modules
module load python/3.7
module load gcc 
module load mpi4py

## activate vitual env
source ~/HDDM/bin/activate 

## cd to the directory from which sbatch was run from
cd $SLURM_SUBMIT_DIR

## execute job
python __PYNAME__ > __OUTPATH____LOGNAME__


