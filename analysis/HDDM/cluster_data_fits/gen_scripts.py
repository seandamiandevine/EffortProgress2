
import pandas as pd
from copy import deepcopy

# ****************************************************************************
# *                                CONSTANTS                                 *
# ****************************************************************************

ACCOUNT   = "sdevine"
NCHAIN    = 1
NSAMPLE   = 5000
NBURN     = 2000

with open('template_hddm.py') as f:
    TEMP_PY_FILE = f.read()

with open('template.sh') as f:
    TEMP_SH_FILE = f.read()

# ****************************************************************************
# *                       Generate Vanilla DDM Scripts                       *
# ****************************************************************************

# Model to fit 
OUTCOMES  = ['a','v','t'] 
BASE_REGS = [
	'y ~ 1',
	'y ~ 1 + showprog_c',
	'y ~ 1 + showprog_c + progress_c',
	'y ~ 1 + showprog_c + progress_c + progress_c2',
	'y ~ 1 + showprog_c + progress_c + showprog_c:progress_c',
	'y ~ 1 + showprog_c + progress_c + progress_c2 + showprog_c:progress_c',
	'y ~ 1 + showprog_c + progress_c + progress_c2 + showprog_c:progress_c + showprog_c:progress_c2',
]

MODELS = {'a':[], 'v':[], 't':[]}
for y in OUTCOMES:
	for mod in BASE_REGS:
		MODELS[y].append(mod.replace('y',y))

MOD_SPACE_DDM = [ [a,v,t] for a in MODELS['a'] for v in MODELS['v'] for t in MODELS['t'] ]

### Save model space
pd.DataFrame(data={'mod':MOD_SPACE_DDM}).to_csv('model_space_ddm.csv', index=False)


### Write scripts
OUT_PATH = f'/home/{ACCOUNT}/scratch/effprog2/exp1ab/'

for i,mod in enumerate(MOD_SPACE_DDM):
	for c in range(NCHAIN):
		
		## py scripts
		FNAME_PY = f'scripts/py/hddm_mod{i}_c{c+1}.py'
		NEW_FILE = deepcopy(TEMP_PY_FILE)
		NEW_FILE = NEW_FILE.replace('__MODTYPE__', '"ddm"')
		NEW_FILE = NEW_FILE.replace('__NSAMPLE__', str(NSAMPLE))
		NEW_FILE = NEW_FILE.replace('__NBURN__', str(NBURN))
		NEW_FILE = NEW_FILE.replace('__REGS__', str(mod))
		NEW_FILE = NEW_FILE.replace('__MODNAME__', f'"mod_{i}_{c+1}"')
		NEW_FILE = NEW_FILE.replace('__OUTPATH__', OUT_PATH)

		with open(FNAME_PY,'w') as f:
			f.write(NEW_FILE)

		## bash scripts
		FNAME_SH = f'scripts/bash/run_hddm{i}_c{c+1}.sh'
		NEW_FILE = deepcopy(TEMP_SH_FILE)
		NEW_FILE = NEW_FILE.replace('__JOBNAME__', f'hddm_mod{i}_c{c+1}')
		NEW_FILE = NEW_FILE.replace('__MAILTYPE__', 'FAIL')
		NEW_FILE = NEW_FILE.replace('__PYNAME__', FNAME_PY)
		NEW_FILE = NEW_FILE.replace('__LOGNAME__', f'logs/hddm_mod{i}_c{c+1}.log')
		NEW_FILE = NEW_FILE.replace('__OUTPATH__', OUT_PATH)

		with open(FNAME_SH,'w') as f:
			f.write(NEW_FILE)

# ****************************************************************************
# *                      # Generate angle model scripts                      *
# ****************************************************************************


OUTCOMES  = ['a','v','t', 'theta'] 

# winning model
MODELS = {'a':[], 'v':[], 't':[], 'theta':[]}
for y in OUTCOMES:
	for mod in BASE_REGS:
		MODELS[y].append(mod.replace('y',y))

MOD_SPACE_ANG = [ [a,v,t,th] for a in MODELS['a'] for v in MODELS['v'] for t in MODELS['t'] for th in MODELS['theta']]

### Save model space
pd.DataFrame(data={'mod':MOD_SPACE_ANG}).to_csv('model_space_angle.csv', index=False)
pd.DataFrame(data={'mod':MOD_SPACE_DDM+MOD_SPACE_ANG}).to_csv('full_model_space.csv', index=False)

## Write angle scripts
for i,mod in enumerate(MOD_SPACE_ANG):
	for c in range(NCHAIN):
		
		## py scripts
		FNAME_PY = f'scripts/py/hddm_angle_mod{i}_c{c+1}.py'
		NEW_FILE = deepcopy(TEMP_PY_FILE)
		NEW_FILE = NEW_FILE.replace('__MODTYPE__', '"angle"')
		NEW_FILE = NEW_FILE.replace('__NSAMPLE__', str(NSAMPLE))
		NEW_FILE = NEW_FILE.replace('__NBURN__', str(NBURN))
		NEW_FILE = NEW_FILE.replace('__REGS__', str(mod))
		NEW_FILE = NEW_FILE.replace('__MODNAME__', f'"angle_mod_{i}_{c+1}"')
		NEW_FILE = NEW_FILE.replace('__OUTPATH__', OUT_PATH)

		with open(FNAME_PY,'w') as f:
			f.write(NEW_FILE)

		## bash scripts
		FNAME_SH = f'scripts/bash/run_hddm_angle{i}_c{c+1}.sh'
		NEW_FILE = deepcopy(TEMP_SH_FILE)
		NEW_FILE = NEW_FILE.replace('__JOBNAME__', f'hddm_angle_mod{i}_c{c+1}')
		NEW_FILE = NEW_FILE.replace('__MAILTYPE__', 'FAIL')
		NEW_FILE = NEW_FILE.replace('__PYNAME__', FNAME_PY)
		NEW_FILE = NEW_FILE.replace('__LOGNAME__', f'logs/hddm_angle_mod{i}_c{c+1}.log')
		NEW_FILE = NEW_FILE.replace('__OUTPATH__', OUT_PATH)

		with open(FNAME_SH,'w') as f:
			f.write(NEW_FILE)
