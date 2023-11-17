# Cluster-distributed HDDM analysis.

A large number of HDDMs were fit for the current project (2744 to be precise), not to mention the 100 simulated HDDM for parameter recovery. As such, not all of the fit trace files are included here; **only the ones from the winning model**. Nevertheless, all of the code provided here would allow someone with access to a computing cluster to replicate our analyses. Namely: 

- `cluster_data_fits/` contains the scripts to fit the HDDMs to (distributively, across multiple CPUs) the empirical data from experiments 1 and 2. Of particular interest, `DICs.csv` contains the calculated DIC values for every HDDM model (see `fx/fx.py` for DIC calculation) and `find_winning_model.py` contains all the analysis of the winning model.
    - `figs/` contains model figures that show up in the manuscript.
    - `fx/` contains custom Python functions used in model comparison and interpretation.
    - `mod_out/` contains .csv summaries of model output (with and without) random effects.
    - `scripts` contains scripts generated by `gen_scripts.py`. Both `bash` files (to run the python file on the cluster) and `python` files (to fit the HDDM). 
    - `traces` contains raw traces for models.
    - `DICs.csv` contains all the DIC values for each fit HDDM (see `fx/fx.py` for DIC calculation).
    - `exp1ab_clean.csv` is a cleaned dataset combining data from experiments 1 and 2. 
    - `find_winning_model.py` is a python script to compare models and interpret and visualize the winning model's parameters. 
    - `gen_scripts.py` generates all HDDM scripts and bash scripts to be fit. This includes all possible fixed effect combinations. 
    - `run_all_scripts.py` is a convenience script to be run on the cluster that simply runs every script in `scripts/bash/`. 
    - `template_hddm.py` is the basic template for each HDDM. Any double-underscored variable (e.g., `__VARIABLE__`) is replaced in `gen_scripts.py`
    - `template.sh` is the basic template for bash scripts. 

- `param_recov/` contains the scripts and results from the (distributed) parameter recovery procedure. These files follow the same basic structure as listed above. 

For security reasons (i.e., not revealing sensitive compute canada account information), some information may be missing. If you have any trouble at all understanding how these models were fit, please contact Sean at seandamiandevine@gmail.com. Don't be shy!

