import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt 
import seaborn as sns
from scipy.stats import gaussian_kde
import hddm
import os
from tqdm import tqdm

os.chdir('/Users/sean/documents/EffProg2/exp1_local/analysis')

plt.style.use('grayscale')
matplotlib.rcParams.update({'font.size': 18})
matplotlib.rcParams['figure.figsize'] = (10.4, 6.8)
matplotlib.rcParams['lines.linewidth'] = 2.5
matplotlib.rcParams['axes.prop_cycle'] = matplotlib.cycler(color=['0', '0.5']) 

pd.options.mode.chained_assignment = None  # ignore chaining warning; default='warn'               

# ****************************************************************************
# *                           Load and clean data                            *
# ****************************************************************************

dat = pd.read_csv('ddms/data_exc.csv')
dat['subj_idx'] = dat['subject']
dat['repsonse'] = dat['accuracy']

dat = dat[~dat.rt.isna()]
dat = dat[dat.rt > 0]
dat['rt'] /= 1000

dat['showprog_c']  = dat.showprog.astype(float)-0.5
dat['progress_c']  = dat.progress - 0.5
dat['progress_c2'] = dat.progress_c ** 2

# ****************************************************************************
# *                                Fit HDDMs                                 *
# ****************************************************************************

regs = {
    'linear_avt':
        ['a ~ showprog_c + progress_c + showprog_c:progress_c', 
         'v ~ showprog_c + progress_c + showprog_c:progress_c', 
         't ~ showprog_c + progress_c + showprog_c:progress_c'], 
    'quadratic_a':
        ['a ~ showprog_c + progress_c + progress_c2 + showprog_c:progress_c + showprog_c:progress_c2', 
         'v ~ showprog_c + progress_c + showprog_c:progress_c', 
         't ~ showprog_c + progress_c + showprog_c:progress_c'], 
    'quadratic_v':
        ['a ~ showprog_c + progress_c + showprog_c:progress_c', 
         'v ~ showprog_c + progress_c + progress_c2 + showprog_c:progress_c + showprog_c:progress_c2', 
         't ~ showprog_c + progress_c + showprog_c:progress_c'],
    'quadratic_t':
        ['a ~ showprog_c + progress_c + showprog_c:progress_c', 
         'v ~ showprog_c + progress_c + showprog_c:progress_c', 
         't ~ showprog_c + progress_c + progress_c2 + showprog_c:progress_c + showprog_c:progress_c2'], 
    'quadratic_av':
        ['a ~ showprog_c + progress_c + progress_c2 + showprog_c:progress_c + showprog_c:progress_c2', 
         'v ~ showprog_c + progress_c + progress_c2 + showprog_c:progress_c + showprog_c:progress_c2', 
         't ~ showprog_c + progress_c + showprog_c:progress_c'], 
    'quadratic_at':
        ['a ~ showprog_c + progress_c + progress_c2 + showprog_c:progress_c + showprog_c:progress_c2', 
         'v ~ showprog_c + progress_c + showprog_c:progress_c', 
         't ~ showprog_c + progress_c + progress_c2 + showprog_c:progress_c + showprog_c:progress_c2'], 
    'quadratic_vt':
        ['a ~ showprog_c + progress_c + showprog_c:progress_c', 
         'v ~ showprog_c + progress_c + progress_c2 + showprog_c:progress_c + showprog_c:progress_c2', 
         't ~ showprog_c + progress_c + progress_c2 + showprog_c:progress_c + showprog_c:progress_c2'], 
    'quadratic_avt':
        ['a ~ showprog_c + progress_c + progress_c2 + showprog_c:progress_c + showprog_c:progress_c2', 
         'v ~ showprog_c + progress_c + progress_c2 + showprog_c:progress_c + showprog_c:progress_c2', 
         't ~ showprog_c + progress_c + progress_c2 + showprog_c:progress_c + showprog_c:progress_c2'], 
}


DICs = {}
for name,model in regs.items():
    ddm = hddm.models.HDDMRegressor(dat, model)
    ddm.find_starting_values()
    ddm.sample(2000, burn=500, dbname=f'ddms/models/traces_{name}', db='pickle')
    ddm.save(f'ddms/models/{name}_N={dat.subject.unique().shape[0]}')

# ****************************************************************************
# *                            Compare model fits                            *
# ****************************************************************************



# choose winning model
winning_mod = 'quadratic_v'
ddm = hddm.load(f'ddms/{winning_mod}__hddm_N=23')

# ****************************************************************************
# *                                Statistics                                *
# ****************************************************************************

# add p-values and gewekes
ddm_summary = ddm.gen_stats()

fig    = plt.figure(1, figsize=[30,30], tight_layout=True)
pars   = ddm_summary[~ddm_summary.index.str.contains('Intercept_')].index.to_list()
traces = ddm.nodes_db.node[[i for i in pars]]

ddm_summary['p_err']  = ddm_summary['mc err']/ddm_summary['std']
ddm_summary['geweke'] = np.nan
ddm_summary['P']      = np.nan

for i,p in enumerate(traces):
    trace = p.trace()

    # ax = fig.add_subplot(round(len(pars)/9), 9, i+1)
    # ax.plot(trace)
    # ax.set(xlabel='', ylabel='', title=pars[i])

    # geweke
    m1,m2 = np.mean(trace[:int(trace.shape[0]*.5)]), np.mean(trace[int(trace.shape[0]*.9):])
    v1,v2 = np.var(trace[:int(trace.shape[0]*.5)]), np.var(trace[int(trace.shape[0]*.9):])
    z = (m2-m1)/np.sqrt(v2+v1)

    # p-value
    p_lt_0 = np.mean(trace < 0)
    p      = p_lt_0 if ddm_summary.loc[pars[i]]['mean'] < 0 else 1-p_lt_0

    # save
    ddm_summary.loc[pars[i], 'geweke'] = z
    ddm_summary.loc[pars[i], 'P'] = 1-p # to match frequentist interpretation

# fig.savefig('figs/traceplots_fullfit.png')
ddm_summary.to_csv(f'ddms/stats/{winning_mod}_summary.csv')
ddm_summary[~ddm_summary.index.str.contains('Intercept_')].to_csv(f'ddms/stats/{winning_mod}_summary_nointercept.csv')



# ****************************************************************************
# *                               Errorbar plot                              *
# ****************************************************************************

titles = {'a':'Decision Threshold', 'v':'Drift Rate', 't':'Non-Decision Time'}

fig,ax = plt.subplots(1,3, figsize=[15,6])

for i,p in enumerate(['a','v','t']):
    tmp = ddm_summary[ddm_summary.index.str[0]==p]
    tmp = tmp[~tmp.index.str.contains('Intercept')]
       
    tmp['lb'] = tmp['mean'] - tmp['2.5q']
    tmp['ub'] = tmp['97.5q'] - tmp['mean']
    ci = tmp[['lb','ub']].T.to_numpy()

    ax[i].errorbar(tmp.index.to_list(), tmp['mean'], fmt='o', yerr=ci, ms=10)
    ax[i].axhline(0, linestyle='--', color='grey', alpha=0.7)
    ax[i].set_xticklabels(tmp.index.to_list(), rotation=90, size=12)
    ax[i].tick_params(axis='y', which='major', labelsize=12)
    ax[i].set(title=titles[p])

    if i ==0:
        ax[i].set(ylabel=r'$\beta$')

fig.subplots_adjust(bottom=.4)

plt.show()
fig.savefig(f'figs/ddm/summary_{winning_mod}.png')
plt.close()


# ****************************************************************************
# *                        Compute parameter estimates                       *
# ****************************************************************************

X = {'showprog':[], 'progress':[]}
for cond in [False,True]:
    for p in range(1,101):
        X['showprog'].append(cond)
        X['progress'].append(p/100)


X = pd.DataFrame(X)
X['showprog_c']  = X.showprog.astype(float)-.5
X['progress_c']  = X.progress-.5
X['progress_c2'] = X.progress_c**2

for p in ['a','v','t']:
    tmp = ddm_summary[ddm_summary.index.str[0]==p]
    tmp = tmp[~tmp.index.str.contains('Intercept')]

    pred = np.zeros((X.shape[0], tmp.shape[0]))
    for i,par in enumerate(tmp.index.to_list()):
        b = tmp.loc[par,'mean']
        pname = par[2:]

        if ':' in pname:
            varnames = pname.split(':')
            out = X[varnames[0]].copy()
            for v in varnames[1:]:
                out*=X[v]

            X[pname] = out

        pred[:,i] = b*X[pname]

    b0   = ddm_summary.loc[f'{p}_Intercept','mean']
    X[p] = b0 + pred.sum(axis=1)
    X[f'{p}_z'] = (X[p]-X[p].mean())/X[p].std()


# ****************************************************************************
# *                           Parameter prediction                           *
# ****************************************************************************

titles = {'a':'Decision Threshold', 'v':'Drift Rate', 't':'Non-Decision Time'}
fig,ax = plt.subplots(1,3,figsize=[15,6], sharey=True)

for i,p in enumerate(['a','v','t']):

    sns.lineplot(x=X['progress'], y=X[f'{p}_z'], hue=X['showprog'], ci=None, palette=('darkgray','darkgreen'), ax=ax[i])
    ax[i].set(xlabel='Progress', ylabel='Predicted Par. Value (Z)', title=titles[p],xticks=[0,.5,1])

    if i==0:
        ax[i].legend(title='Progress?')
    else:
        ax[i].legend([],[], frameon=False)

plt.show()
fig.savefig(f'figs/{winning_mod}_parameter_predictions.png')
plt.close()


# ****************************************************************************
# *                           PPC (Non-Hiearchical)                          *
# ****************************************************************************

np.random.seed(2022)

X['rt']  = np.zeros(X.shape[0])
X['acc'] = np.zeros(X.shape[0])

for i in tqdm(range(X.shape[0]),desc='simulating PPC...'):
    a, v, t       = X[['a','v','t']].iloc[i]
    pred,_        = hddm.generate.gen_rand_data({'a':a,'v':v,'t':t}, size=1000)
    pred.rt.iloc[0]
    X.rt.iloc[i]  = pred.rt.mean()
    X.acc.iloc[i] = pred.response.mean().round()

# Plot
fig, ax = plt.subplots(1)
X['progbin'] = pd.qcut(X.progress,10, labels=False)/10+.1
sns.lineplot(x=X['progbin'], y=X['rt'], hue=X['showprog'], ci=None, palette=('darkgray','darkgreen'), ax=ax)
ax.set(xlabel='Progress', ylabel='Simulated RT', title=titles[p],xticks=[0,.5,1])
ax.legend(title='Progress?')

plt.show()
fig.savefig(f'figs/{winning_mod}_PPC.png')
plt.close()


# ****************************************************************************
# *                             PPC (Hiearchical)                            *
# ****************************************************************************
np.random.seed(2022)

X2 = []
for subject in dat.subject.unique():
    X['subject'] = subject
    X2.append(X)

X2        = pd.concat(X2)
X2['rt']  = np.zeros(X2.shape[0])
X2['acc'] = np.zeros(X2.shape[0])

for i in tqdm(range(X2.shape[0]),desc='simulating PPC...'):
    sub, a, v, t  = X2[['subject','a','v','t']].iloc[i]
    a0, v0, t0    = ddm_summary.loc[[f'{p}_Intercept' for p in ['a','v','t']]]['mean'] 
    Uaj, Uvj, Utj = ddm_summary.loc[[f'{p}_Intercept_subj.{int(sub)}' for p in ['a','v','t']]]['mean'] 
    a, v, t       = a+a0-Uaj, v+v0-Uvj, t+t0-Utj

    pred,_         = hddm.generate.gen_rand_data({'a':a,'v':v,'t':t}, size=1000)
    X2.rt.iloc[i]  = pred.rt.mean()
    X2.acc.iloc[i] = pred.response.mean().round()

# Plot
fig, ax = plt.subplots(1)
X2['progbin'] = pd.qcut(X2.progress,10, labels=False)/10+.1
X2 = X2.reset_index()
sns.lineplot(x=X2['progbin'], y=X2['rt'], hue=X2['showprog'], ci=None, palette=('darkgray','darkgreen'), ax=ax)
ax.set(xlabel='Progress', ylabel='Simulated RT', title=titles[p],xticks=[0,.5,1])
ax.legend(title='Progress?')

plt.show()
fig.savefig(f'figs/{winning_mod}_PPC.png')
plt.close()


