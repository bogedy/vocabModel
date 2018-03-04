#change this to project directory
setwd("C:/Users/Isaiah/eclipse-workspace/vocab model and lyric scraping")
data=read.csv("RapSheet.csv")
attach(data)
location=as.factor(location)
decade=as.factor(decade)
#create a full model using sample size, location, and decade born
full_model=lm(vocabsize~samplesize+location+decade)
summary(full_model)
#make a reduced model. seems that location is more important than decade born.
reduced_model=lm(vocabsize~samplesize+location)
summary(reduced_model)
anova(reduced_model)
anova(full_model)
#compute F statistic to see if reduced model is better:
((anova(reduced_model)[3,2]-anova(full_model)[4,2])/(reduced_model$df.residual-full_model$df.residual))/(anova(full_model)[4,2]/full_model$df.residual)
#F statistic is 0.3505684
anova(reduced_model,full_model)
#huge p-value for the f-test! he do not reject the null, that the reduced model is better.