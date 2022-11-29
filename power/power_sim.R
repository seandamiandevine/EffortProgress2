library(lme4); library(lmerTest)
set.seed(2022)

# Define constants ----------------------------------------------------------------

Ns     = seq(5,50,by=5)
ntrial = 60
nsim   = 100

G00  = 500  # overall RT
TAU0 = 25   

G10  = -10  # fixed showprog effect 
TAU1 = 0   

G20  = 50   # fixed linear progress effect
TAU2 = 0  

G30  = -60  # fixed quadratic progress effect
TAU3 = 0  

G40  = 10   # fixed reward effect
TAU4 = 0   

G50  = -50  # fixed showprog X progress
TAU5 = 0   

G60  = -100  # fixed showprog_c X progress_c2
TAU6 = 0   

R    = 100  # residual variance


## Visualize linear prediction -----

X = expand.grid(showprog = c(-.5,.5), progress=seq(-.5,.5,length.out=60), 
                reward = c(-.5, .5))
X$progress2 = X$progress^2

y = G00 + G10*X$showprog + G20*X$progress + G30*X$progress2 + G40*X$reward + 
    G50*(X$showprog*X$progress) + G60*(X$showprog*X$progress2)

m = tapply(y, list(X$progress+.5, X$showprog), mean)
colnames(m) = c('No Progress', 'Progress')

pdf('figs/linear_prediction.pdf',width=6,height=6)

matplot(m, type='l', col=c('darkgrey', 'darkgreen'), lwd=3, lty=1,
        xlab = 'Proximity', ylab='Predicted Correct RT. (ms.)', main='Linear Prediction', 
        xaxt='n')
axis(1, at=seq(0,60,length.out=3), labels = c(0,.5,1))
legend('topleft', bty='n', lty=1, col=c('darkgrey', 'darkgreen'), lwd=3, 
       title='', legend=colnames(m))

dev.off()

# Simulate ----------------------------------------------------------------

output = data.frame()

for(n in Ns) {
  cat('\n\n****** sample size: ', n, '****** \n')
  
  X = expand.grid(showprog = c(0,1), progress=seq(0,1,length.out=60), 
                  reward = c(0, 1), id=1:n)
  
  X$showprog_c  = X$showprog-.5
  X$reward_c    = X$reward-.5
  X$progress_c  = X$progress-.5
  X$progress_c2 = X$progress_c^2
  
  pb = txtProgressBar(min = 0, max=nsim, width=50, style=3)
  for(sim in 1:nsim) {
    setTxtProgressBar(pb, sim)

    b0 = rnorm(n, G00, TAU0)
    b1 = rnorm(n, G10, TAU1)
    b2 = rnorm(n, G20, TAU2)
    b3 = rnorm(n, G30, TAU3)
    b4 = rnorm(n, G40, TAU4)
    b5 = rnorm(n, G50, TAU5)
    b6 = rnorm(n, G60, TAU6)
    
    pred_rt = sapply(1:n, function(i) {
      b0[i] + b1[i]*X[X$id==i, 'showprog_c'] + b2[i]*X[X$id==i, 'progress_c'] + 
      b3[i]*X[X$id==i, 'progress_c2'] + b4[i]*X[X$id==i, 'reward_c'] + 
      b5[i]*(X[X$id==i, 'showprog_c'] * X[X$id==i, 'progress_c']) + 
      b6[i]*(X[X$id==i, 'showprog_c'] * X[X$id==i, 'progress_c2']) + 
      rnorm(length(X[X$id==i, 'showprog_c']), 0, R)
      }
    )
    
    X$rt = c(pred_rt)
    
    # model 
    tryCatch(
      {
        mod = lmer(rt ~ showprog_c*(progress_c + progress_c2) + reward_c + (1|id), data=X)
      }, error = function(cond) {
        next
      }
    )

    # save
    bs = t(as.data.frame(fixef(mod)))
    rownames(bs) = NULL
    colnames(bs) = paste0('b_', colnames(bs))
    
    ps = t(as.data.frame(summary(mod)$coefficients[,'Pr(>|t|)']))
    rownames(ps) = NULL
    colnames(ps) = paste0('p_', colnames(ps))
    
    o      = as.data.frame(cbind(bs, ps))
    o$sim  = sim
    o$N    = n
    output = rbind(output, o)
  }
}

write.csv(output, paste0('power_sim_', min(Ns), '-', max(Ns),'.csv'))


# Visualize ---------------------------------------------------------------

# output = read.csv('power_sim_5-50.csv')

alpha   = 0.05
opt_pwr = .8
pars    = names(output[grepl('p_', names(output))])
pars    = pars[!grepl('Intercept', pars)]
pwr     = reshape2::melt(output[,c('N', pars)], id.vars='N')
pwr$sig = as.numeric(pwr$value < alpha)

psig      = tapply(pwr$sig, list(pwr$N, pwr$variable), mean)
req_ns    = sapply(1:ncol(psig), function(i) as.numeric(names(which(psig[,i]>=opt_pwr))[1]))
names(req_ns) = colnames(psig)
data.frame(req_ns)


pars_l = c('Prog. Cond', 'Proximity','Proximity^2','Reward', 
           'Prog. Cond. X Proximity', 'Prog. Cond. X Proximity^2')
#pars_l = paste0(pars_l, ' (n = ',unname(req_ns), ')')

pdf('figs/power_curves.pdf',width=6,height=6)

cols = rainbow(ncol(psig))
matplot(rownames(psig), psig, type='l', lwd=5, lty=1, col='black', 
        xlab='Sample Size', ylab='P(Significant)', ylim=c(0,1), yaxt='n')
matplot(rownames(psig), psig, type='l', lty=1, pch=16, lwd=2, 
        col=cols, add=T)
axis(2, at=seq(0,1,by=.2), labels=seq(0,1,by=.2))
abline(h=opt_pwr, lty=2)
legend('bottomright', col=cols, lty=1, legend=gsub('p_','', pars_l),lwd=3,cex=1)

dev.off()
