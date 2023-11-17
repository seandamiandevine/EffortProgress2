#!/bin/bash -login

## account to use
#SBATCH --account=def-rotto

## walltime HH:MM:SS
#SBATCH -t 168:00:00

## nodes
#SBATCH --cpus-per-task=1

## memory
#SBATCH --mem-per-cpu=15G

## email notification
#SBATCH --mail-user=seandamiandevine@gmail.com
#SBATCH --mail-type=FAIL

## save SLURM output to specified directory
#SBATCH --output=logs/%j.log  

## load relevant modules
module load python/3.7
module load gcc 
module load mpi4py

## activate vitual env
source ~/HDDM/bin/activate 

## cd to the directory from which sbatch was run from
cd $SLURM_SUBMIT_DIR

## execute job
python param_recovery.py


