import os
from glob import glob
from time import sleep

S = 100 ## number of simulations 

for i in range(S):
	os.system('sbatch run_param_recov.sh')
	sleep(1)
