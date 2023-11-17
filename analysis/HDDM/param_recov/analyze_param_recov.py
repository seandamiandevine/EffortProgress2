import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
from tqdm import tqdm

recov = pd.read_csv("recovered_pars.csv")
recov = recov.dropna()

recov.columns = recov.columns.str.strip() ## remove whitespaces

# Get parameters
pars = pd.unique(['_'.join(c.split("_")[1:]) for c in recov.columns if 'true' in c])

# Loop through and compare
fig, ax = plt.subplots(4,6,figsize=(15,10), constrained_layout=True) ## one row per par

a_count  = 0
v_count  = 0
th_count = 0
t_count  = 0
for p in tqdm(pars):
	true  = recov[f"true_{p}"].values
	est   = recov[f"est_{p}"].values

	# pick row
	if p.startswith('a_'): 
		this_ax = ax[0,a_count]
		a_count+=1
	elif p.startswith('v_'):
		this_ax = ax[1,v_count]
		v_count+=1
	elif p.startswith('t_'):
		this_ax = ax[2,t_count]
		t_count+=1
	elif p.startswith('theta_'):
		this_ax = ax[3,th_count]
		th_count+=1

	sns.regplot(x=true,y=est,ax=this_ax,ci=None,scatter_kws={"color": "grey"}, line_kws={"color": "red"})
	this_ax.set(xlabel="", ylabel="", title=p)

	r = pearsonr(true,est)
	this_ax.text(0.1, 0.9, 
		f'r = {r[0]:.2f}\np = {r[1]:.4f}',
		horizontalalignment='left',
		verticalalignment='center',
		transform = this_ax.transAxes)

	
## remove blank plots
fig.delaxes(ax[0,5])
fig.delaxes(ax[2,5])
fig.delaxes(ax[3,4])
fig.delaxes(ax[3,5])

fig.supxlabel("True Value")
fig.supylabel("Estimated Value")

fig.savefig("figs/param_recov.pdf")
