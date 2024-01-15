#load data
setwd(dir = "")

Gautier_Data<-read.csv2("Gautier_Data.csv")
str(Gautier_Data)
Gautier_Data$method<-as.factor(Gautier_Data$method)

#libraries
library(multcompView)
library(readxl)
library(ggplot2)
library(reshape2)
library(corrplot)
library(RColorBrewer)
library(dplyr)
library(broom)
library(ggeffects)
library(stargazer)
library(ggfortify)
library(lsmeans)
library(emmeans)
library(ggplot2)
library(Hmisc)
library(vegan)
library(ggsci)
library(sandwich)
library(msm)

####Exploratory data######
#Check the variability of the customized precision formula
ggplot(data=Gautier_Data, aes(y = precision, x = method, fill = method)) +
  geom_boxplot(fill = c("#DA5724","cyan")) + geom_jitter(color="black", alpha=0.9) + theme_bw()
GBXMethod<-Gautier_Data[1:31,]
TervurenMethod<-Gautier_Data[32:59,]
GBXMethod <- GBXMethod$precision
TervurenMethod <- TervurenMethod$precision

#Test_Stats
t.test(GBXMethod,TervurenMethod)
# ==> Significant test so there is a precision value that is different with the TERVUREN method

#same on absolute value
ggplot(data=Gautier_Data, aes(y = absolute_precision, x = method, fill = method)) +
  geom_boxplot(fill = c("#DA5724","cyan")) + geom_jitter(color="black", alpha=0.9) + theme_bw()
GBXMethod<-Gautier_Data[1:31,]
TervurenMethod<-Gautier_Data[32:59,]
GBXMethod <- GBXMethod$absolute_precision
TervurenMethod <- TervurenMethod$absolute_precision

#Test_Stats
t.test(GBXMethod,TervurenMethod)
# ==> Significant test so there is a precision value that is different with the TERVUREN method

ggplot(data=Gautier_Data, aes(y = heightmean, x = method, fill = method)) +
  geom_boxplot(fill = c("orange","#DA5724")) + geom_jitter(color="black", alpha=0.9)

#Hmin = Valeur de seuil minimal
#S = Saturation
#V = Valeur min to maximal
#Blur = Flou
#Erodex = Rogner
#Erodey = Rogenr
#Aremin = Aire minimal pour qu'un compteur soit pris
#Airemax = seuil maximum
#widthmean = Largeur moyenne des contours sélectionnés
#heightmean = Hauteur moyennes des contours sélectionnés

#LM
pairs2(Gautier_Data[,c(17 : 27)])

lm.preci<- lm(precision ~ widthmean + size_conservation + counting_zone + density + overlap + variability +colored_variability, data = Gautier_Data)
summary(lm.preci)
lm.preci<- lm(absolute_precision ~ real_density, data = Gautier_Data)
summary(lm.preci)


#Modèle mixte en fonction du site

ggplot(data=Gautier_Data, aes(y = precision, x = size_conservation)) +
  geom_point(shape = 1) +
  geom_smooth(method = "lm",se = T, color = "black")+
  theme_bw()

ggplot(data=Gautier_Data, aes(y = precision, x = overlap)) +
  geom_point(shape = 1) +
  geom_smooth(method = "lm",se = T, color = "black")+
  theme_bw()

ggplot(data=Gautier_Data, aes(y = precision, x = real_density, fill = method)) +
  geom_point(shape = 1) +
  geom_smooth(method = "lm",se = T, color = "black")+
  theme_bw()

ggplot(data=Gautier_Data, aes(y = precision, x = Blur)) +
  geom_point(shape = 1) +
  geom_smooth(method = "lm",se = T, color = "black")+
  theme_bw()


ggplot(data=Gautier_Data, aes(y = precision, x = Blur)) +
  geom_point(shape = 1) +
  geom_smooth(method = "lm",se = T, color = "black")+
  theme_bw()


ggplot(data=Gautier_Data, aes(y = real_number, x = algo_number, fill = method)) +
  geom_point(shape = 1) +
  geom_smooth(method = "lm",se = T, color = "black")+ geom_abline(slope = 1, intercept = 0, size = 1, color = "red") +
  theme_bw()

ggplot(data=Gautier_Data, aes(y = precision, x = Erodex, fill = method)) +
  geom_point(shape = 1) +
  geom_smooth(method = "lm",se = T, color = "black")+
  theme_bw()

ggplot(data=Gautier_Data, aes(y = absolute_precision, x = real_number, fill = method)) +
  geom_point(shape = 1) +
  geom_smooth(method = "lm",se = T, color = "black")+
  theme_bw()

