### Assumes HDDM > 0.9!!
import pandas as pd
import numpy as np
import hddm
from hddm.simulators.hddm_dataset_generators import simulator_h_c

# Metadata
MODEL     = 'angle'
N_SUBJ    = 60
N_TRIALS  = 1000
N_ITER    = 5000
N_BURN    = 2000

# Regression model
# should be the winning model from the empirical fits

a_reg  = {"model":'a ~ 1 + showprog_c + progress_c + progress_c2 + showprog_c:progress_c', 'link_func':lambda x:x}
v_reg  = {"model":'v ~ 1 + showprog_c + progress_c + progress_c2 + showprog_c:progress_c + showprog_c:progress_c2', 'link_func':lambda x:x}
t_reg  = {"model":'t ~ 1 + showprog_c + progress_c + progress_c2 + showprog_c:progress_c', 'link_func':lambda x:x}
th_reg = {"model":'theta ~ 1 + showprog_c + progress_c + progress_c2', 'link_func': lambda x:x}

REG_MODS =  [a_reg,v_reg,t_reg,th_reg] 


# ****************************************************************************
# *                                 Simulate                                 *
# ****************************************************************************

regression_covariates = {
    'showprog_c' : {'type': 'categorical', 'range': (-0.5, 0.5)},
    'progress_c' : {'type': 'continuous',  'range': (-0.5, 0.5)},
    'progress_c2': {'type': 'continuous',  'range': (0, 1)}
    }

sim_data, param_dict = simulator_h_c(
    n_subjects=N_SUBJ,
    n_trials_per_subject=N_TRIALS,
    # data=X,
    model=MODEL,
    conditions=None,
    depends_on=None,
    regression_models=[x['model'] for x in REG_MODS],
    regression_covariates=regression_covariates,
    group_only_regressors=True,
    p_outlier=0.00
)

fixef_names = []
for m in [x['model'] for x in REG_MODS]:
    parname   = m.split(" ~ ")[0]
    prednames = m.split("~")[-1].split(" + ")[1:]
    prednames = ['Intercept'] + prednames
    prednames = [f'{parname}_{pred}' for pred in prednames]
    fixef_names+=prednames

true_fixefs = {f'true_{k}': param_dict[k] for k in fixef_names} ## save generative parameters

# ****************************************************************************
# *                                 Fit model                                *
# ****************************************************************************

ddmnn = hddm.HDDMnnRegressor(sim_data,
                             REG_MODS,
                             include = hddm.simulators.model_config[MODEL]['hddm_include'],
                             model   = MODEL,
                             informative = False)
ddmnn.find_starting_values()
ddmnn.sample(N_ITER, burn=N_BURN)

## Generate fit summary
pars_sum = ddmnn.gen_stats() ## estimated parameters

## Append to csv
true_df = pd.DataFrame(true_fixefs, index=[0])
est_df  = pd.DataFrame(pars_sum[pars_sum.index.isin(fixef_names)]['mean'])
est_df.index = 'est_'+est_df.index
est_df = est_df.T
est_df = est_df.reset_index(drop=True)

par_recov = pd.concat([true_df,est_df],axis=1)

with open('recovered_pars.csv', 'a') as f:
    f.write('\n')  ## add new lines
par_recov.to_csv('recovered_pars.csv', mode='a', header=False, index=False) ## append results






