import os
import pandas as pd
from glob import glob
from time import sleep

LIMIT = 1000 # beluga has a 1000 job limit, so only run up to the first 1000

# identify which files have already been fit
DICs = pd.read_csv('DICs.csv')
all_scripts  = glob('scripts/bash/*.sh')

script_names = []
for f in all_scripts:
	if 'angle' in f:
		script_names.append(f.replace('_c','_').replace("angle","").replace('run_hddm','angle_mod').split('/')[-1].replace('.sh',''))
	else:
		script_names.append(f.replace('_c','_').replace('run_hddm','mod_').split('/')[-1].replace('.sh',''))

unfit_files  = [all_scripts[i] for i,n in enumerate(script_names) if n not in DICs.model.to_list()]

# run all unfit files
for i,f in enumerate(unfit_files):
	if i+1 == LIMIT:
		# kill at job LIMIT-1
		break

	os.system(f'sbatch {f}')
	sleep(1)

