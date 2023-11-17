
import pandas as pd
import numpy as np
import pickle
import hddm
import re
from tqdm import tqdm
from hddm.simulators.basic_simulator import simulator
from hddm.simulators.hddm_dataset_generators import hddm_preprocess
from statsmodels.stats.weightstats import ztest

def hddm_summary(fname, perc=[.025,.975], geweke_prop = [.1,.5], burn=0):

	"""
	hddm.load() doesn't allow you to specify an alternative path for the trace file, which is 
	problematic when loading from compute canada. 
	
	
	These are functions that bypass that behaviour and reproduce parameter summaries from the raw traces.
	
	https://github.com/hddm-devs/kabuki/blob/995e1c519b150fc1802d7fe7d10447d4caccb24d/kabuki/utils.py#L32
	
	TODO: 
	    - how to modify the pickle file to fix the trace pointer...
	
	"""

	# load trace
	with open(fname, "rb") as f:
		trace_dict = pickle.loads(f.read())

	del trace_dict['_state_']
	del trace_dict['deviance']

	trace_dict = { k:trace_dict[k][0] for k in trace_dict.keys() }
	trace_df   = pd.DataFrame(trace_dict)

	# remove burnin
	trace_df = trace_df.iloc[burn:]

	# produce summary
	summary = trace_df.describe(percentiles=perc).T

	# p-value
	p_val = lambda x: (x<0).mean() if (x<0).mean()<.5 else 1-(x<0).mean()
	summary['P'] = trace_df.apply(lambda x: p_val(x))

	# geweke
	n      = trace_df.shape[0]
	bounds = (int(geweke_prop[0]*n), int(geweke_prop[1]*n))
	geweke = trace_df.apply(lambda x: ztest(x[:bounds[0]], x[bounds[1]:])[0])
	summary["Geweke"] = geweke

	# sort
	summary = summary.sort_index()

	# return
	return summary,trace_df



def get_model_str(mod_name:str) -> list:

	x = mod_name.split('_')[1]
	with open(f'scripts/py/hddm_mod{x}_c1.py', 'r') as f:
		lines = f.read()

	mod_list = eval(re.search("REG_MODS = (.*)",lines).group(1))
	return mod_list


def parEst(ddm_summary):

	# create DM
	X = {'showprog':[], 'progress':[]}
	for cond in [False,True]:
		for p in range(1,101):
			X['showprog'].append(cond)
			X['progress'].append(p/100)

	X = pd.DataFrame(X)
	X['showprog_c']  = X.showprog.astype(float)-.5
	X['progress_c']  = X.progress-.5
	X['progress_c2'] = X.progress_c**2

	# summary
	# ddm_summary = mod.gen_stats()

	# estimate
	pars = ddm_summary.index.str.split('_').str[0].unique()
	pars = pars[pars!='z']

	for p in pars:
		tmp = ddm_summary[ddm_summary.index.str.split("_").str[0]==p]
		tmp = tmp[~tmp.index.str.contains('Intercept')]

		pred    = np.zeros((X.shape[0], tmp.shape[0]))
		pred_ub = np.zeros((X.shape[0], tmp.shape[0]))
		pred_lb = np.zeros((X.shape[0], tmp.shape[0]))
		for i,par in enumerate(tmp.index.to_list()):
		    b   = tmp.loc[par,'mean']
		    blb = tmp.loc[par,'2.5%']
		    bub = tmp.loc[par,'97.5%']
		    pname = "_".join(par.split("_")[1:])

		    if ':' in pname:
		        varnames = pname.split(':')
		        out = X[varnames[0]].copy()
		        for v in varnames[1:]:
		            out*=X[v]

		        X[pname] = out

		    pred[:,i]    = b*X[pname]
		    pred_ub[:,i] = bub*X[pname]
		    pred_lb[:,i] = blb*X[pname]

		b0   = ddm_summary.loc[f'{p}_Intercept','mean']
		b0lb = ddm_summary.loc[f'{p}_Intercept','2.5%']
		b0ub = ddm_summary.loc[f'{p}_Intercept','97.5%']
		X[p] = b0 + pred.sum(axis=1)

	X['showprog'] = np.where(X['showprog']==False, 'No Progress', 'Progress')

	return X



def PPC(ddm_summary, data=None, seed:int=2023, hierarchical=True, bias=True, model='ddm', n_sim=10):

	np.random.seed(seed)

	# Create DM
	if hierarchical:
		X = data.copy()
		X['rt_hat']  = np.zeros(X.shape[0])
		X['acc_hat'] = np.zeros(X.shape[0])
	else:
		X = {'showprog':[], 'progress_c':[], 'progress_c2':[]}
		n = data.progress_c.unique().shape[0]
		for cond in [False,True]:
			for p in range(n):
				X['showprog'].append(cond)
				X['progress_c'].append(data.progress_c.unique()[p])
				X['progress_c2'].append(data.progress_c2.unique()[p])

		X = pd.DataFrame(X)
		X['showprog_c']  = X.showprog.astype(float)-.5
		X['subj_idx']    = 0
		X['rt_hat']      = 0
		X['acc_hat']     = 0

	#  Make parameter predictions
	pars = ddm_summary.index.str.split('_').str[0].unique()
	pars = pars[pars!='z']
	for p in pars:
		tmp  = ddm_summary[ddm_summary.index.str.split("_").str[0]==p]
		tmp  = tmp[~tmp.index.str.contains('Intercept')]
		pred = np.zeros((X.shape[0], tmp.shape[0]))
		for i,par in enumerate(tmp.index.to_list()):
		    b = tmp.loc[par,'mean']
		    pname = "_".join(par.split("_")[1:])

		    if ':' in pname:
		        varnames = pname.split(':')
		        out = X[varnames[0]].copy()
		        for v in varnames[1:]:
		            out*=X[v]
		        X[pname] = out

		    pred[:,i] = b*X[pname]

		if hierarchical:
			b0 = ddm_summary.loc[[f'{p}_Intercept_subj.{sub}' for sub in X.subj_idx], 'mean'].tolist()
			b0 = np.array(b0, dtype=float)
		else:
			b0 = ddm_summary.loc[f'{p}_Intercept','mean']
		X[p] = b0 + pred.sum(axis=1)

	if bias: 
		# get bias term
		if hierarchical:
			X['z'] = ddm_summary.loc[[f'z_subj.{sub}' for sub in X.subj_idx], 'mean'].tolist()
		else:
			X['z'] = ddm_summary.loc['z','mean']
	else: 
		X['z'] = 0

	# Simualte using the simulator() function
	if model=='ddm':
		theta = np.array([X['v'].values, X['a'].values, X['z'].values, X['t'].values]).T
	elif model=='angle':
		theta = np.array([X['v'].values, X['a'].values, X['z'].values, X['t'].values, X["theta"].values]).T

	rts,resps,info = simulator(theta=theta, model=model,n_samples=n_sim)
	rts   = rts.squeeze()
	resps = resps.squeeze()
	resps[resps==-1] = 0

	X['rt_hat']  = rts.mean(axis=0)
	X['acc_hat'] = resps.mean(axis=0)

	return X








