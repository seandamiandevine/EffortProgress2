
library(lme4)
library(lmerTest)
rm(list = ls())

setwd("~/Documents/EffProg2/exp1_local/analysis/a")

# Load data ---------------------------------------------------------------

files = paste0('data/', list.files('data/'))
dat   = do.call(plyr::rbind.fill, lapply(files, read.csv))
dat   = dat[dat$isDataTrial=="true", ]
dat   = dat[!is.na(dat$trial_type),]
dat   = dat[dat$block!='practice', ]

se = function(x) sd(x,na.rm=T)/sqrt(length(x))

# Exclusion ---------------------------------------------------------------

qust = dat[,grepl('\\d', names(dat))]
dat  = dat[,!grepl('\\d', names(dat))]

NT   = length(unique(dat$subject))

dat$rt      = as.numeric(dat$rt)
dat$timeout = ifelse(is.na(dat$rt), 1, 0)

dat$block = as.numeric(dat$block)
dat = transform(dat,
                ptimeout = ave(dat$timeout, list(dat$subject, dat$block), FUN=mean),
                pcorrect = ave(dat$accuracy, list(dat$subject, dat$block), FUN=mean)
                )


Oacc      = round(tapply(dat$accuracy, dat$subject, mean),2)
Ort       = tapply(dat$rt, dat$subject, mean, na.rm=T)
ptimeout  = tapply(dat$timeout, dat$subject, mean)
rmv       = unique(c(names(ptimeout[ptimeout > 0.25]), # 30% or more timeouts
                     names(Oacc[Oacc < 0.44]),         # 33% accuracy
                     names(Ort[Ort < 100])))           # on average faster than 100ms



## Pre-exclusion descriptive plots ----
pdf('figs/rt_hist_pre_exc.pdf',width=6,height=6)

mrt = tapply(dat$rt, dat$subject, mean, na.rm=T)
hist(mrt, main='Avg. RTs (ms.)', xlab='', freq = F, xlim=c(0,1000))
abline(v=100, lty=2, lwd=2)

dev.off()

pdf('figs/acc_hist_pre_exc.pdf',width=6,height=6)

Oacc = tapply(dat$accuracy, dat$subject, mean)
hist(Oacc, main = 'P(Correct)', xlim=c(0,1), xlab='')
abline(v=0.44, lty=2, lwd=2)

dev.off()

pdf('figs/ptimeout_pre_exc.pdf',width=6,height=6)

ptimeout = tapply(dat$timeout, dat$subject, mean)
hist(ptimeout, main = 'P(Timeout)', xlim=c(0,1), xlab='')
abline(v=1/3, lty=2, lwd=2)

dev.off()

dat = dat[!dat$subject %in% rmv,]
# write.csv(dat, 'ddms/data_exc.csv') # for hddm


# Descriptives ------------------------------------------------------------

desc = list(
  N         = length(unique(dat$subject)),
  mage      = mean(unique(ifelse(as.numeric(dat$age) > 1000, 2022-as.numeric(dat$age), as.numeric(dat$age))), na.rm=T), 
  sdage     = sd(unique(ifelse(as.numeric(dat$age) > 1000, 2022-as.numeric(dat$age), as.numeric(dat$age))), na.rm=T),
  sexes     = mean(grepl('f', tolower(dat$gender))),
  Nexc      = 40 -length(unique(dat$subject)) ,
  Ntrials   = table(dat$subject),
  maxTok    = tapply(dat$totalTokens, dat$subject, max),
  instQ     = tapply(dat$totalInstQ, dat$subject, unique),
  Oacc      = Oacc,
  times     = tapply(dat$time_elapsed, dat$subject, max)/60000,
  comments  = tapply(dat$comments, dat$subject, unique),
  strategy  = tapply(dat$strategy, dat$subject, unique)
)

names(desc$comments) = NULL; names(desc$strategy) = NULL
capture.output(desc,file='out/descriptives.txt')


# RT/acc dist -----------------------------------------------------------
pdf('figs/rt_hist.pdf',width=6,height=6)

cor = dat[dat$accuracy==1, ]
hist(cor$rt, main='Correct RTs (ms.)', xlab='', freq = F)
lines(density(cor$rt,na.rm=T), lwd=2)

dev.off()

pdf('figs/acc_hist.pdf',width=6,height=6)

Oacc = tapply(dat$accuracy, dat$subject, mean)
hist(Oacc, main = 'P(Correct)', xlim=c(0,1), xlab='')
abline(v=1/3, lty=2, lwd=2)
legend('topleft', bty='n', lty=2,lwd=2, legend='Chance')

dev.off()

pdf('figs/cond_acc_plot.pdf',width=6,height=6)

dat    = dat[dat$timedout=='false',]
q      = quantile(dat$rt, probs = seq(0, 1, length.out=20), na.rm=T)
rtbin  = cut(dat$rt, breaks=q, labels = F, include.lowest = T)
binlab = round(tapply(dat$rt, rtbin, mean))
pcor  = tapply(dat$accuracy, rtbin, mean)
secor = tapply(dat$accuracy, rtbin, se)

plot(pcor, type='b', xaxt='n', xlab='RT (ms.)', ylim=c(0,1), ylab='P(Correct)', 
     main='Conditional Accuracy\n(no timeouts)', pch=15)
axis(1, at=1:length(binlab), labels = binlab)

dev.off()

pdf('figs/rt_across_blocks.pdf',width=6,height=6)

cor$block = as.numeric(cor$block)
mrt = tapply(cor$rt, cor$block, mean)
plot(names(mrt), mrt, type='b', pch=16, xlab='Block', main='Mean Correct RT (ms.)', ylab='', 
     ylim=range(pretty(mrt)))

dev.off()

pdf('figs/acc_across_blocks.pdf',width=6,height=6)

dat$block = as.numeric(dat$block)
macc = tapply(dat$accuracy, dat$block, mean)
plot(names(macc), macc, type='b', pch=16, xlab='Block', main='P(Correct)', ylab='', ylim=c(0,1))

dev.off()

# Progress effect ---------------------------------------------------------

nbin    = 5
progdat = dat[dat$progress > .10, ] # remove first 0.1 of trials

## RT basic group difference ----

progcor = progdat[progdat$accuracy==1, ] # only the end
progbin = cut(progcor$progress,10, labels=F)
mrt     = tapply(progcor$rt, list(progbin, progcor$showprog), mean, na.rm=T)
sert    = tapply(progcor$rt, list(progbin, progcor$showprog), se)
mrt     = mrt[c(5,10),]
sert    = sert[c(5,10),]
yrange  = c(500, 560) #range(pretty(c(mrt-sert-10, mrt+sert)))

pdf('figs/rt_progress_effects_basic_barplot.pdf',width=6,height=6)

b = barplot(mrt, beside=T, ylim=yrange, xpd=F, names.arg =c('No Progress', 'Progress'), 
            xlab='', ylab='Avg. Correct RT (ms.)', 
            legend.text = T, 
            args.legend = list(x='topright',  bty='n',cex=1.5, legend=c('Middle of Block', 'End of Block')))
arrows(b, mrt-sert, b, mrt+sert, length=0)

dev.off()

### model ----
progcor$progbin_c  = ifelse(progbin %in% c(5,10), progbin, NA)
progcor$progbin_c  = ifelse(progcor$progbin_c==5, -.5, .5)
progcor$showprog_c = ifelse(progcor$showprog=='false', -.5, .5)

progcor = progcor[progcor$rt > 0,]
progcor$logrt = log(progcor$rt)

rt_lmer0 = lmer(logrt ~ 1 + (1|subject), data=progcor[!is.na(progcor$progbin_c),])
rt_lmer1 = lmer(logrt ~ showprog_c + (1|subject), data=progcor[!is.na(progcor$progbin_c),])
rt_lmer2 = lmer(logrt ~ progbin_c+showprog_c + (1|subject), data=progcor[!is.na(progcor$progbin_c),])
rt_lmer3 = lmer(logrt ~ progbin_c*showprog_c + (1|subject), data=progcor[!is.na(progcor$progbin_c),])

anova(rt_lmer0, rt_lmer1, rt_lmer2, rt_lmer3)
summary(rt_lmer3)
sjPlot::tab_model(rt_lmer3, file='out/rt_basic_lmer.html')

## Accuracy basic group difference ----

progbin  = cut(progdat$progress,10, labels=F)
macc     = tapply(progdat$accuracy, list(progbin, progdat$showprog), mean, na.rm=T)
seacc    = tapply(progdat$accuracy, list(progbin, progdat$showprog), se)
macc     = macc[c(5,10),]
seacc    = seacc[c(5,10),]
yrange   = c(0.5,1)#range(pretty(c(macc-seacc-.1, macc+seacc+.1)))

pdf('figs/accuracy_progress_effects_basic_barplot.pdf',width=6,height=6)

b = barplot(macc, beside=T, ylim=yrange, xpd=F, names.arg =c('No Progress', 'Progress'), 
            xlab='', ylab='P(Correct)', 
            legend.text = T, 
            args.legend = list(x='topright',  bty='n',cex=1.5, legend=c('Middle of Block', 'End of Block')))
arrows(b, macc-seacc, b, macc+seacc, length=0)

dev.off()

### model ----
progdat$progbin_c  = ifelse(progbin %in% c(5,10), progbin, NA)
progdat$progbin_c  = ifelse(progdat$progbin_c==5, -.5, .5)
progdat$showprog_c = ifelse(progdat$showprog=='false', -.5, .5)

acc_lmer0 = glmer(accuracy ~ 1 + (1|subject), data=progdat[!is.na(progdat$progbin_c), ], family='binomial')
acc_lmer1 = glmer(accuracy ~ showprog_c + (1|subject), data=progdat[!is.na(progdat$progbin_c), ], family='binomial')
acc_lmer2 = glmer(accuracy ~ progbin_c+showprog_c + (1|subject), data=progdat[!is.na(progdat$progbin_c), ], family='binomial')
acc_lmer3 = glmer(accuracy ~ progbin_c*showprog_c + (1|subject), data=progdat[!is.na(progdat$progbin_c), ], family='binomial')

anova(acc_lmer0, acc_lmer1, acc_lmer2, acc_lmer3)
sjPlot::tab_model(acc_lmer3, file='out/acc_basic_glmer.html')

## RT binned ----
pdf('figs/rt_progress_bin_ribbon.pdf',width=6,height=6)

progcor = progdat[progdat$accuracy==1, ]
progbin = cut(progcor$progress, nbin, labels = F)
binlab  = seq(0,1,length.out=nbin)

mrt     = tapply(progcor$rt, list(progbin, progcor$showprog), mean, na.rm=T) 
sert    = tapply(progcor$rt, list(progbin, progcor$showprog), se) 
yrange  = range(pretty(c(mrt-sert, mrt+sert)))

matplot(mrt, xlab = 'P(Bar Filled)', ylab='Mean RT (ms.)', 
        col=c('darkgrey', 'darkgreen'), xaxt='n', lty=1, type='b', ylim=yrange, 
        lwd=3, pch=18, cex=2)
axis(1,at=1:nbin,labels=binlab)
legend('topleft',bty='n', col=c('darkgrey', 'darkgreen'), lty=1, lwd=2, cex=1.5, legend=c('No Progress', 'Progress'))

x = 1:length(binlab)
l = mrt-sert
u = mrt+sert

polygon(c(x, rev(x)), c(l[,1], rev(u[,1])), col = scales::alpha('darkgrey', 0.25), lty = 0)
polygon(c(x, rev(x)), c(l[,2], rev(u[,2])), col = scales::alpha('darkgreen', 0.25), lty = 0)

dev.off()

## Acc binned ----

pdf('figs/acc_progress_bin_ribbon.pdf',width=6,height=6)

progbin = cut(progdat$progress, nbin, labels = F)
binlab  = seq(0,1,length.out=nbin)

macc   = tapply(progdat$accuracy, list(progbin, progdat$showprog), mean, na.rm=T) 
seacc  = tapply(progdat$accuracy, list(progbin, progdat$showprog), se) 
yrange = c(.8,1)#range(pretty(c(macc-seacc, macc+seacc)))

matplot(macc, xlab = 'P(Bar Filled)', ylab='P(Correct)', 
        col=c('darkgrey', 'darkgreen'), xaxt='n', lty=1, type='b', ylim=yrange, 
        lwd=3, pch=18, cex=2)
axis(1,at=1:nbin,labels=binlab)
legend('topleft',bty='n', col=c('darkgrey', 'darkgreen'), lty=1, lwd=2, cex=1.5, legend=c('No Progress', 'Progress'))

x = 1:length(binlab)
l = macc-seacc
u = macc+seacc

polygon(c(x, rev(x)), c(l[,1], rev(u[,1])), col = scales::alpha('darkgrey', 0.25), lty = 0)
polygon(c(x, rev(x)), c(l[,2], rev(u[,2])), col = scales::alpha('darkgreen', 0.25), lty = 0)


dev.off()

## RT effects across full duration  ----

pdf('figs/rt_progress_cont.pdf',width=6,height=6)

progcor$block = as.numeric(progcor$block)
k    = 15

mv_rt = c()
for(i in unique(progcor$subject)) {
  for(j in unique(progcor$block)) {
    tmp = progcor[progcor$subject==i & progcor$block==j,]
    
    mv_rt = c(mv_rt, zoo::rollmean(tmp$rt, k=k, fill = NA, align='right'))
  }
}

progcor$mv_rt = mv_rt

mrt  = tapply(progcor$mv_rt, list(progcor$progress, progcor$showprog), mean, na.rm=T)
sert = tapply(progcor$mv_rt, list(progcor$progress, progcor$showprog), se)
colnames(mrt) = c('No Progress','Progress')
start = as.numeric(rownames(mrt[!is.na(mrt[,1]),,drop=F]))[1]
yrange = c(500, 560) #range(pretty(c(mrt-sert, mrt+sert)))

matplot(rownames(mrt), mrt, type='l', pch=16,lty=1,col=c('darkgrey','darkgreen'),
        xlab='P(Bar Filled)', ylab='Moving Avg. of Correct RT', lwd=2,
        ylim=yrange,xlim=c(start,1))

x = as.numeric(rownames(mrt))
polygon(x=c(x, rev(x)), y=c(mrt[,1] - sert[,1], rev(mrt[,1]+sert[,1])),
        col=scales::alpha('darkgrey', 0.11), border = 0)
polygon(x=c(x, rev(x)), y=c(mrt[,2] - sert[,2], rev(mrt[,2]+sert[,2])),
        col=scales::alpha('darkgreen', 0.11), border = 0)

legend('topleft', bty='n', lty=1, col=c('darkgrey', 'darkgreen'), title='', cex=1.5,
       legend=colnames(mrt), lwd=2)

dev.off()

## Acc effects across full duration ----
pdf('figs/acc_progress_cont.pdf',width=6,height=6)

k   = 5
progdat = progdat[progdat$progress >= .2,]
progdat$block  = as.numeric(progdat$block)

mv_acc = c()
for(i in unique(progdat$subject)) {
  for(j in unique(progdat$block)) {
    tmp = progdat[progdat$subject==i & progdat$block==j,]
    
    mv_acc = c(mv_acc, zoo::rollmean(tmp$accuracy, k=k, fill = NA, align='right'))
  }
}

progdat$mv_acc = mv_acc

macc  = tapply(progdat$mv_acc, list(progdat$progress, progdat$showprog), mean, na.rm=T)
seacc = tapply(progdat$mv_acc, list(progdat$progress, progdat$showprog), se)
colnames(macc) = c('No Progress','Progress')
start = as.numeric(rownames(macc[!is.na(macc[,1]),,drop=F]))[1]
yrange = range(pretty(c(macc-seacc, macc+seacc)))

matplot(rownames(macc), macc, type='l', pch=16,lty=1,col=c('darkgrey','darkgreen'),
        xlab='P(Bar Filled)', ylab='Moving Avg. of P(Correct)',
        ylim=yrange,xlim=c(start,1))

x = as.numeric(rownames(macc))
polygon(x=c(x, rev(x)), y=c(macc[,1] - seacc[,1], rev(macc[,1]+seacc[,1])),
        col=scales::alpha('darkgrey', 0.11), border = 0)
polygon(x=c(x, rev(x)), y=c(macc[,2] - seacc[,2], rev(macc[,2]+seacc[,2])),
        col=scales::alpha('darkgreen', 0.11), border = 0)

legend('bottomright', bty='n', lty=1, col=c('darkgrey', 'darkgreen'), title='',cex=1.5,
       legend=colnames(macc), ncol=2)


dev.off()

# Reward ------------------------------------------------------------------

nbin    = 5
progdat = dat[dat$progress > .10, ] # remove first 0.1 of trials

## RT ----
progcor = progdat[progdat$accuracy==1, ]
progbin = cut(progcor$progress, nbin, labels = F)
binlab  = round(tapply(progcor$progress, progbin, mean),2)

mrt     = tapply(progcor$rt, list(progbin, progcor$reward, progcor$showprog), mean, na.rm=T) 
sert    = tapply(progcor$rt, list(progbin, progcor$reward, progcor$showprog), se) 
yrange  = range(pretty(c(mrt-sert, mrt+sert)))

pdf('figs/rt_progress_reward_effects_noprog.pdf',width=6,height=6)

matplot(mrt[,,1], xlab = 'P(Bar Filled)', ylab='Mean RT (ms.)', 
        col=c('red', 'blue'), pch=16, xaxt='n', lty=1, type='b', ylim=yrange, main='No Progress')
arrows(1:nbin,mrt[,1,1]-sert[,1,1],1:nbin,mrt[,1,1]+sert[,1,1],length=0, col='red')
arrows(1:nbin,mrt[,2,1]-sert[,2,1],1:nbin,mrt[,2,1]+sert[,2,1],length=0, col='blue')
axis(1,at=1:nbin,labels=binlab)
legend('topleft',bty='n', col=c('red', 'blue'), lty=1, legend=colnames(mrt[,,1]))

dev.off()

pdf('figs/rt_progress_reward_effects_prog.pdf',width=6,height=6)

matplot(mrt[,,2], xlab = 'P(Bar Filled)', ylab='Mean RT (ms.)', 
        col=c('red', 'blue'), pch=16, xaxt='n', lty=1, type='b', ylim=yrange, main='Progress')
arrows(1:nbin,mrt[,1,2]-sert[,1,2],1:nbin,mrt[,1,2]+sert[,1,2],length=0, col='red')
arrows(1:nbin,mrt[,2,2]-sert[,2,2],1:nbin,mrt[,2,2]+sert[,2,2],length=0, col='blue')
axis(1,at=1:nbin,labels=binlab)
legend('topleft',bty='n', col=c('red', 'blue'), lty=1, legend=colnames(mrt[,,2]))

dev.off()


## Acc ----
# main
progbin = cut(progdat$progress, nbin, labels = F)
binlab  = round(tapply(progdat$progress, progbin, mean),2)

macc    = tapply(progdat$accuracy, list(progbin, progdat$reward, progdat$showprog), mean, na.rm=T) 
seacc   = tapply(progdat$accuracy, list(progbin, progdat$reward, progdat$showprog), se) 
yrange  = range(pretty(c(macc-seacc, macc+seacc)))

pdf('figs/acc_progress_reward_effects_noprog.pdf',width=6,height=6)

matplot(macc[,,1], xlab = 'P(Bar Filled)', ylab='P(Correct)', 
        col=c('red', 'blue'), pch=16, xaxt='n', lty=1, type='b', ylim=yrange, main='No Progress')
arrows(1:nbin,macc[,1,1]-seacc[,1,1],1:nbin,macc[,1,1]+seacc[,1,1],length=0, col='red')
arrows(1:nbin,macc[,2,1]-seacc[,2,1],1:nbin,macc[,2,1]+seacc[,2,1],length=0, col='blue')
axis(1,at=1:nbin,labels=binlab)
legend('topleft',bty='n', col=c('red', 'blue'), lty=1, legend=colnames(macc[,,1]))

dev.off()

pdf('figs/acc_progress_reward_effects_prog.pdf',width=6,height=6)

matplot(macc[,,2], xlab = 'P(Bar Filled)', ylab='P(Correct)', 
        col=c('red', 'blue'), pch=16, xaxt='n', lty=1, type='b', ylim=yrange, main='Progress')
arrows(1:nbin,macc[,1,2]-seacc[,1,2],1:nbin,macc[,1,2]+seacc[,1,2],length=0, col='red')
arrows(1:nbin,macc[,2,2]-seacc[,2,2],1:nbin,macc[,2,2]+seacc[,2,2],length=0, col='blue')
axis(1,at=1:nbin,labels=binlab)
legend('topleft',bty='n', col=c('red', 'blue'), lty=1, legend=colnames(macc[,,2]))

dev.off()

# Quadratic MLM -----------------------------------------------------------
## RT  ----
### Fit-----
cor = dat[dat$accuracy==1,]
cor$showprog_c  = ifelse(cor$showprog=='false', -.5, .5)
cor$progress_c  = cor$progress-.5
cor$reward_c    = ifelse(cor$reward==1, .5, -.5)
cor$progress_c2 = cor$progress_c^2

cor = cor[cor$rt > 0, ]
cor$logrt = log(cor$rt)

rt_q_mod0   = lmer(logrt ~ 1 + (1|subject), data=cor)
rt_q_mod1   = lmer(logrt ~ showprog_c + (1|subject), data=cor)
rt_q_mod2   = lmer(logrt ~ showprog_c + progress_c + (1|subject), data=cor)
rt_q_mod3   = lmer(logrt ~ showprog_c + progress_c + reward_c + (1|subject), data=cor)
rt_q_mod4   = lmer(logrt ~ showprog_c * progress_c + reward_c + (1|subject), data=cor)
rt_q_mod5   = lmer(logrt ~ showprog_c  + progress_c + progress_c2 + showprog_c:progress_c + showprog_c:progress_c2 + reward_c + (1|subject), data=cor) 

anova(rt_q_mod0, rt_q_mod1, rt_q_mod2, rt_q_mod3, rt_q_mod4, rt_q_mod5)
summary(rt_q_mod5)
car::Anova(rt_q_mod5)

sjPlot::tab_model(rt_q_mod5, file='out/rt_q_mod.html')

### Visualize ----
png('figs/quadratic_mlm_rt.png', units='in', width=4, height=4, res=400)

X = data.frame(showprog_c  = rep(c(-.5,.5), each=100),
               progress_c = rep(seq(-.5,.5,length.out=100), 2), 
               progress_c2 = rep(seq(-.5,.5,length.out=100)^2, 2),
               reward_c = 0, subject=median(unique(cor$subject)))

pred = exp(predict(rt_q_mod5, newdata=X, re.form=NA))

X$progress = X$progress_c+.5
plot(X$progress[X$showprog_c<0], pred[X$showprog_c<0], type='l',
     ylab='Predicted Correct RT', xlab='P(Bar Filled)', col='darkgrey', lwd=4)
lines(X$progress[X$showprog_c>0], pred[X$showprog_c>0], col='darkgreen', lwd=4)
legend('topleft', bty='n', lty=1, lwd=4, col=c('darkgrey', 'darkgreen'),
       legend=c('No Progress', 'Progress'), title='')

dev.off()

## Acc  ----
### Fit ----
dat$showprog_c  = ifelse(dat$showprog=='false', -.5, .5)
dat$progress_c  = dat$progress-.5
dat$reward_c    = ifelse(dat$reward==1, .5, -.5)
dat$progress_c2 = dat$progress_c^2

acc_q_mod0   = glmer(accuracy ~ 1 + (1|subject), data=dat, family='binomial')
acc_q_mod1   = glmer(accuracy ~ showprog_c + (1|subject), data=dat, family='binomial')
acc_q_mod2   = glmer(accuracy ~ showprog_c + progress_c + (1|subject), data=dat, family='binomial')
acc_q_mod3   = glmer(accuracy ~ showprog_c + progress_c + reward_c + (1|subject), data=dat, family='binomial')
acc_q_mod4   = glmer(accuracy ~ showprog_c * progress_c + reward_c + (1|subject), data=dat, family='binomial')
acc_q_mod5   = glmer(accuracy ~ showprog_c  + progress_c + progress_c2 + showprog_c:progress_c + showprog_c:progress_c2 + reward_c + (1|subject), data=dat, family='binomial') 

anova(acc_q_mod0, acc_q_mod1, acc_q_mod2, acc_q_mod3, acc_q_mod4, acc_q_mod5)
anova(acc_q_mod3, acc_q_mod5)

summary(acc_q_mod5)
sjPlot::tab_model(acc_q_mod5, transform = NULL, file='out/acc_q_mod.html')

### Visualize ----
png('figs/quadratic_mlm_acc.png', units='in', width=4, height=4, res=400)

X = data.frame(showprog_c  = rep(c(-.5,.5), each=100),
               progress_c = rep(seq(-.5,.5,length.out=100), 2), 
               progress_c2 = rep(seq(-.5,.5,length.out=100)^2, 2),
               reward_c = 0, subject=median(unique(cor$subject)))

pred = predict(acc_q_mod5, newdata=X, re.form=NA)
pred = exp(pred)/(1+exp(pred))

X$progress = X$progress_c+.5
plot(X$progress[X$showprog_c<0], pred[X$showprog_c<0], type='l',
     ylab='Predicted P(Correct)', xlab='P(Bar Filled)', col='darkgrey', lwd=4, 
     ylim=c(.85,1))
lines(X$progress[X$showprog_c>0], pred[X$showprog_c>0], col='darkgreen', lwd=4)
legend('topright', bty='n', lty=1, lwd=4, col=c('darkgrey', 'darkgreen'),
       legend=c('No Progress', 'Progress'), title='')

dev.off()

