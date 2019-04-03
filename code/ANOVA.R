library(data.table)
options(stringsAsFactors=F)
review.chn = fread("/Users/SX/Documents/AMERICA/STUDY/4th semester/STAT628/Module2/Data/review_train_chinese.csv")
review.chn$text.words = strsplit(review.chn$text,split = " ")
for(i in 1:5){ #barplots of word frequency in each rating category
  words.star = review.chn$text.words[which(review.chn$stars==i)]
  words.star = unlist(words.star)
  words.star.count = sort(table(words.star),decreasing = T)
  png(paste0("/Users/SX/Documents/AMERICA/STUDY/4th semester/STAT628/Module2/Results/Barplots/Barplot_WordsFreq_Star",i,".png"),width = 1000,height = 700)
  barplot(words.star.count[1:20],las=2)
  dev.off()
}

##Merge sentences back to whole review
MergeArray <- function(list){
  a = NULL
  for(i in 1:length(list)){a = c(a,list[[i]])}
  return(a)
}
text.uid = aggregate(text~uid, data = review.chn, FUN = MergeArray)
SplitWords <- function(list){
  a = strsplit(list[[1]],split = " ")
  a = unlist(a)
  a = list(a)
  return(a)
}
words.splited = NULL
for(i in 1:nrow(text.uid)){ ##because lapply doesn't work
  words.splited[i] = SplitWords(text.uid$text[i])
  if(i%%10000==0) print(i)
}
text.uid$text = words.splited #dataframe of text and ID

stars.uid = aggregate(stars~uid, data = review.chn, FUN = mean) #dataframe of stars and ID
review.sub = merge(text.uid, stars.uid, by = "uid") ##merged dataset
uid.bid = review.chn[-which(duplicated(review.chn$uid)),c(1,5)]
review.sub2 = merge(review.sub, uid.bid, by = "uid")

n.review<-function(bid){
  return(sum(review.sub2$bussiness_id==bid))
}
n.review(176386)


attr = read.csv("/Users/SX/Documents/AMERICA/STUDY/4th semester/STAT628/Module2/Data/business_train_attributes_chinese.csv")
attr[attr==""] = "None"
attr[is.na(attr)] = "None"

attr$n.review = sapply(attr$business_id, FUN = n.review)#col of number of reviews in one business
hist(attr$n.review,breaks = 100)

attr = attr[which(attr$n.review>=20),]

n.none<-function(x){return(sum(x=="None"))}
attr$n.none = apply(attr,1,FUN = n.none)#col of number of Nones in one business's attributes

###=======impact of "None"===========
model = lm(stars~n.none, data = attr)
summary(model)
summary(model)$coef[2,4]
#plot(model)
plot(attr$n.none, attr$stars, pch = 16, cex=0.3)
abline(model, col = "red")



#=================Feature Importance and anova==========
FeatureImportance = data.frame(Attributes = c("NoiseLevel","RestaurantsDelivery","BusinessAcceptsCreditCards","Caters","Alcohol",
                                              "HasTV","RestaurantsPriceRange2","lot","BikeParking","RestaurantsReservations",
                                              "OutdoorSeating","street","divey","WiFi","RestaurantsTableService",
                                              "casual","GoodForKids","dinner","WheelchairAccessible","DriveThru",
                                              "brunch","BusinessAcceptsBitcoin","RestaurantsGoodForGroups","touristy","latenight",
                                              "validated","trendy","DogsAllowed","RestaurantsTakeOut","lunch",
                                              "garage","breakfast","RestaurantsAttire","hipster","upscale",
                                              "valet","romantic","dessert","dassy"),
                               ImpoScore = c(116,107,97,91,83,77,70,60,57,55,51,50,48,45,44,42,34,33,27,21,21,20,20,18,14,14,14,13,13,11,11,10,9,9,7,3,3,2,1))
barplot(cumsum(FeatureImportance$ImpoScore[39:1]))

attr.all = data.frame(Attributes = colnames(attr)[3:90], anova.p=NA, ImpoScore=0)
for(i in 3:90){
  if(length(table(attr[i]))>1){
    aov = aov(attr$stars~attr[,i])
    attr.all$anova.p[i-2] = summary(aov)[[1]][1,5]
  }
  if(colnames(attr)[i]%in%FeatureImportance$Attributes) attr.all$ImpoScore[i-2] = FeatureImportance$ImpoScore[which(FeatureImportance$Attributes==colnames(attr)[i])]
  attr.all$n.nonmiss[i-2] = sum(attr[,i]!="None")
}
attr.all = attr.all[order(attr.all$ImpoScore,decreasing = T),]
attr.all$anova.p = signif(attr.all$anova.p,2)
write.csv(attr.all, "./Documents/AMERICA/STUDY/4th semester/STAT628/Module2/Tables/Attributes_ANOVA.csv",row.names = F)

plot(attr.all[attr.all$ImpoScore!=0,]$ImpoScore, -log10(attr.all[attr.all$ImpoScore!=0,]$anova.p), 
     xlab = "Importance Level", ylab = "-log10(p) in ANOVA", main = "-log10(p) vs. Importance Level")
model = lm(-log10(anova.p)~ImpoScore, data = attr.all, subset = attr.all$ImpoScore!=0)
#abline(model, col="red")

attr.selected = attr.all[which(attr.all$anova.p<=0.05/88 & attr.all$ImpoScore>50),]
attr.selected
write.csv(attr.selected,
          "./Documents/AMERICA/STUDY/4th semester/STAT628/Module2/Tables/SelectedAttributes_ANOVA.csv",row.names = F)

#================= spcific checks =====
aggr = aggregate(stars~NoiseLevel, data=attr, FUN=mean)
star.mean = aggr$stars[-3]
names(star.mean) = aggr$NoiseLevel[-3]
barplot(sort(star.mean), col = topo.colors(4,alpha = 0.3), main = "Noise Level", ylab = "Average Ratings")
aov = aov(stars~NoiseLevel, data=attr)
summary(aov)

aggr = aggregate(stars~RestaurantsDelivery, data=attr, FUN=mean) #None
star.mean = aggr$stars
names(star.mean) = aggr$RestaurantsDelivery
barplot(sort(star.mean), col = topo.colors(4,alpha = 0.3), main = "RestaurantsDelivery", ylab = "Average Ratings")
aov = aov(stars~RestaurantsDelivery, data=attr)
summary(aov)

aggr = aggregate(stars~BusinessAcceptsCreditCards, data=attr, FUN=mean) #None
star.mean = aggr$stars
names(star.mean) = aggr$BusinessAcceptsCreditCards
barplot(sort(star.mean), col = topo.colors(4,alpha = 0.3), main = "BusinessAcceptsCreditCards", ylab = "Average Ratings")
aov = aov(stars~BusinessAcceptsCreditCards, data=attr)
summary(aov)

aggregate(stars~Caters, data=attr, FUN=mean) #None
aov = aov(stars~Caters, data=attr)
summary(aov)

aggregate(stars~Alcohol, data=attr, FUN=mean) #None
aov = aov(stars~Alcohol, data=attr)
summary(aov)

aggregate(stars~HasTV, data=attr, FUN=mean) #None
aov = aov(stars~HasTV, data=attr)
summary(aov)

aggregate(stars~RestaurantsPriceRange2, data=attr, FUN=mean)
aov = aov(stars~RestaurantsPriceRange2, data=attr)
summary(aov)

aggregate(stars~lot, data=attr, FUN=mean)
aov = aov(stars~lot, data=attr)
summary(aov)

aggregate(stars~BikeParking, data=attr, FUN=mean)
aov = aov(stars~BikeParking, data=attr)
summary(aov)

aggregate(stars~BikeParking, data=attr, FUN=mean)
aov = aov(stars~BikeParking, data=attr)
summary(aov)




