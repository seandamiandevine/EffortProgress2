import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pickle
import hddm
import re
from glob import glob
from tqdm import tqdm

from fx.fx import *

# Load behavioural data
dat = pd.read_csv('exp1ab_clean.csv')


# ****************************************************************************
# *                             # Model comparison                           *
# ****************************************************************************

## this was originally a larger number to explore the top 5 best models,
## but for the purposes of this repo, we set this to 1 (i.e., the winning model)
N_TOP = 1 

DICs = pd.read_csv('DICs.csv')
DICs = DICs.sort_values('dic')
DICs["model_type"] = np.where(DICs.model.str.contains("angle"), "Collapsing Bounds", "Standard")
top_mods = DICs.model.iloc[:N_TOP].to_list()

fig, ax = plt.subplots(1, figsize=(8,4), constrained_layout=True)

lim = (DICs.dic.min()-6000, DICs.dic.quantile(0.99)+4000)
sns.barplot(data=DICs, x='model', y='dic', hue="model_type", ax=ax, errorbar=None)
ax.set(xticks=[],
 ylim=lim, 
 xlabel='', 
 ylabel=('DIC\n'r'$\longleftarrow$ Better Fit                     Worse Fit $\longrightarrow$'))
ax.legend(title="Model Type", loc="upper left")

# plt.show()
fig.savefig("figs/DICs.pdf", transparent=True)
plt.close()

# ****************************************************************************
# *                           # Stats and figs                               *
# ****************************************************************************

for i,mod_name in enumerate(top_mods):

	## Load model from fit_models/ 
	x = re.match(r'^(\w+)_\d+$', mod_name).group(1)

	# mod = hddm.load(f'fit_models/{x}_1.hddm')
	stats,traces = hddm_summary(f'traces/traces/traces_{x}_1.db',burn=0)

	## Save stats
	# stats = mod.gen_stats()
	stats.to_csv(f"mod_out/{mod_name}_stats.csv")
	stats[~stats.index.str.contains('_subj|_std|_trans')].to_csv(f'mod_out/{mod_name}_summary_nointercept.csv')

	## Get parnames for plotting
	parnames = stats.index.str.split("_").str[0].unique()
	if 'theta' in parnames:
		# reorder for plots
		parnames = ['a','v','t','theta']
	else:
		parnames = ['a','v','t']


	## Dot plot
	fixef_pars = stats[~stats.index.str.contains('Intercept|_subj|_std|_trans')]
	fixef_pars['par'] = fixef_pars.index

	fig, ax = plt.subplots(1,len(parnames),figsize=(10,4), constrained_layout=True)

	for i,p in enumerate(parnames):
		if len(fixef_pars[fixef_pars.index.str.contains(f'{p}_')])==0:
			continue 

		pars = fixef_pars[fixef_pars.index.str.contains(f'{p}_')]
		if 'theta' in parnames and p=='a':
			pars = pars[~pars.index.str.contains(f'theta_')]

		pars.loc[:,'par'] = pars.par.str.replace(f'{p}_', '')
		pars.loc[:,'par'] = pars.par.str.replace(f'_c', '')
		sns.pointplot(ax=ax[i], data=pars, 
			 x='mean',
			 y='par', 
			 linestyles='', 
			 color='grey')

		for j in range(pars.shape[0]):
			x = (pars['2.5%'].iloc[j],pars['97.5%'].iloc[j])
			y = (j,j)
			ax[i].plot(x,y, c='red')
		ax[i].axvline(0, ls='--', c='grey', alpha=0.5)
		ax[i].set(xlabel='', ylabel='', title=p)
		ax[i].tick_params(axis='y', which='major', labelsize=8)

	fig.suptitle(f'{mod_name}')
	# plt.show()
	fig.savefig(f'figs/{mod_name}_pointplot.pdf')
	plt.close()

	## Traceplots
	fixef_trace =  traces[fixef_pars.index]

	ncol = 5
	nrow = int(np.ceil(fixef_trace.shape[1] / ncol))

	fig, axs = plt.subplots(nrow, ncol, figsize=(12,6), constrained_layout=True, sharex=True)
	for i, ax in enumerate(axs.flat):
		if i>(fixef_trace.shape[1]-1):
			ax.plot([],[])
			ax.axis('off')
			continue
		ax.plot(fixef_trace.iloc[:,i], c='grey')
		ax.axhline(fixef_trace.iloc[:,i].mean(), c='red')
		ax.set(xlabel='Sample', ylabel='', title=fixef_trace.columns[i])

	fig.suptitle(f'{mod_name}')
	# plt.show()
	fig.savefig(f'figs/{mod_name}_traceplot.pdf')
	plt.close()

	## Parameter estimates
	X = parEst(stats)

	titles = {'a':'Decision Threshold', 'v':'Drift Rate', 't':'Non-Decision Time','theta':"Boundary Collapse Angle"}
	fig,ax = plt.subplots(1,len(parnames),figsize=[12,4], constrained_layout=True)

	for i,p in enumerate(parnames):

		if i==0:
			ylab="Predicted Value"
		else:
			ylab=""

		sns.lineplot(x=X['progress'], y=X[f'{p}'], hue=X['showprog'], errorbar=None,
			palette=('darkgray','darkgreen'), ax=ax[i])
		ax[i].set(xlabel='P(Bar Filled)', ylabel=ylab, title=titles[p],xticks=[0,.5,1], 
			ylim=[np.round(X[f'{p}'].min()-.01,2), np.round(X[f'{p}'].max()+.01,2)])

		if i==0:
		    ax[i].legend(framealpha=0)
		else:
		    ax[i].legend([],[], frameon=False)

		fig.suptitle(mod_name)
		# plt.show()
		fig.savefig(f'figs/{mod_name}_parameter_predictions.pdf',transparent=True)
		plt.close()

	## PPC
	if 'theta' in parnames:
		model = "angle"
	else: 
		model = "ddm"
	X = PPC(ddm_summary=stats, data=dat, hierarchical=True, bias=True, model=model)

	nbin = 6
	X['progbin']   = pd.qcut(X.progress_c,nbin, labels=False)
	X['proglab']   = np.where(X.showprog_c==.5,'Progress', 'No Progress')
	dat['progbin'] = pd.qcut(dat.progress_c,nbin, labels=False)
	dat['proglab'] = np.where(dat.showprog_c==.5,'Progress', 'No Progress')

	fig, ax = plt.subplots(1, 2, figsize=(8,4), constrained_layout=True)

	# RT 
	sns.lineplot(data=X, x='progbin', y='rt_hat', hue='proglab', ax=ax[0], 
		palette=['darkgrey', 'darkgreen'],errorbar=None, legend=False)

	sns.lineplot(data=dat, x='progbin', y='rt', hue='proglab', ax=ax[0], 
		palette=['darkgrey', 'darkgreen'], linestyle='--', errorbar=None, legend=False)
	
	ax[0].set(xlabel='Progress', ylabel='Correct RT',#ylim=[0.3,.8],
		xticks=range(nbin), xticklabels=np.round(np.linspace(0,1,num=nbin),2))
	
	# Acc
	sns.lineplot(data=X, x='progbin', y='acc_hat', hue='proglab', ax=ax[1], 
		palette=['darkgrey', 'darkgreen'],errorbar=None, legend=True)

	sns.lineplot(data=dat, x='progbin', y='response', hue='proglab', ax=ax[1], 
		palette=['darkgrey', 'darkgreen'], linestyle='--', errorbar=None, legend=False)

	ax[1].set(xlabel='Progress', ylabel='P(Correct)', ylim=(.5,1),
		xticks=range(nbin), xticklabels=np.round(np.linspace(0,1,num=nbin),2))

	ax[1].plot([],[], c='black', ls='--', label='Behaviour')
	ax[1].plot([],[], c='black', ls='-', label='Model')
	ax[1].legend(loc='lower right',title='', ncol=2)

	fig.suptitle(mod_name)
	
	# plt.show()
	fig.savefig(f'figs/{mod_name}_PPC.pdf',transparent=True)
	plt.close()
	

	### alternative plotting for PPC
	fig, ax = plt.subplots(2, 2, figsize=(8,5), constrained_layout=True, sharex=True)

	# RT 
	sns.lineplot(data=X, x='progbin', y='rt_hat', hue='proglab', ax=ax[0,0], 
		palette=['darkgrey', 'darkgreen'],errorbar=None, legend=False)

	sns.lineplot(data=dat, x='progbin', y='rt', hue='proglab', ax=ax[1,0], 
		palette=['darkgrey', 'darkgreen'], errorbar=None, legend=False)
	
	ax[0,0].set(xlabel='', title="Predicted", ylabel='Simulated RT',ylim=[0.2,.6],
		xticks=range(nbin), xticklabels=np.round(np.linspace(0,1,num=nbin),2))
	ax[1,0].set(xlabel='Progress', title="Observed", ylabel='Empirical RT',ylim=[0.2,.6],
		xticks=range(nbin), xticklabels=np.round(np.linspace(0,1,num=nbin),2))
	
	# Acc
	sns.lineplot(data=X, x='progbin', y='acc_hat', hue='proglab', ax=ax[0,1], 
		palette=['darkgrey', 'darkgreen'],errorbar=None, legend=False)

	sns.lineplot(data=dat, x='progbin', y='response', hue='proglab', ax=ax[1,1], 
		palette=['darkgrey', 'darkgreen'], errorbar=None, legend=False)
	
	ax[0,1].set(xlabel='', title="Predicted", ylabel='Simulated P(Correct)',ylim=[0.7,1.],
		xticks=range(nbin), xticklabels=np.round(np.linspace(0,1,num=nbin),2))
	ax[1,1].set(xlabel='Progress', title="Observed", ylabel='Empirical P(Correct)',ylim=[0.7,1.],
		xticks=range(nbin), xticklabels=np.round(np.linspace(0,1,num=nbin),2))

	ax[1,1].plot([],[], '-', c="darkgreen", label="Progress")
	ax[1,1].plot([],[], '-', c="darkgrey", label="No Progress")
	ax[1,1].legend(loc="lower left")

	fig.suptitle(mod_name)
	
	# plt.show()
	fig.savefig(f'figs/{mod_name}_PPC2.pdf',transparent=True)
	plt.close()

