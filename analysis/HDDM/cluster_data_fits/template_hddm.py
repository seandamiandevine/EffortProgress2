### Assumes HDDM > 0.9!!

import pandas as pd
import numpy as np
import hddm

# Load data
dat = pd.read_csv('exp1ab_clean.csv', index_col=0)

# Metadata
TYPE   = __MODTYPE__
N_ITER = __NSAMPLE__
N_BURN = __NBURN__
M_NAME = __MODNAME__

# Regressor models
REG_MODS = __REGS__

# Sample! 
ddmnn = hddm.HDDMnnRegressor(dat,
                             REG_MODS,
                             include =  hddm.simulators.model_config[TYPE]['hddm_include'],
                             model = TYPE,
                             informative = False)
ddmnn.sample(N_ITER, burn = N_BURN, dbname=f'__OUTPATH__traces/traces_{M_NAME}.db', db='pickle')

print(f'\n\nDIC = {ddmnn.dic}')

with open('DICs.csv','a') as f: 
    rm_str = str(REG_MODS).replace(',',';')
    f.writelines(f'\n{M_NAME}, {rm_str} , {ddmnn.dic}\n')
    
ddmnn.save(f'__OUTPATH__fit_models/{M_NAME}.hddm')





