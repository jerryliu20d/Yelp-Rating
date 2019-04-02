library(data.table)
review.cleaned = as.data.frame(fread("/z/Comp/lu_group/Members/nshen7/STAT628/Module2/Data/cleaned_review.csv",header = T))
text = review.cleaned$text
text.words = strsplit(text," ")
review.cleaned$text.words = text.words


#==============draw a wordcloud=============
library("wordcloud")
for(i in 1:5){
  words.star = review.cleaned$text.words[which(review.cleaned$stars==i)]
  words.star = unlist(words.star)
  words.star.count = table(words.star)
  sort(words.star.count,decreasing = T)[1:20]
  png(paste0("/z/Comp/lu_group/Members/nshen7/STAT628/Module2/Results/Plots/WordCloud_star",i,".png"),height = 700,width = 700)
  set.seed(1)
  wordcloud(words = rownames(words.star.count), freq = words.star1.count, min.freq = 1,
            max.words=200, random.order=FALSE, rot.per=0.35, 
            colors=brewer.pal(8, "Dark2"))
  dev.off()
  print(i)
}
#=================================================

#=================================================
#===========Find Chinese restaurants==============
business = as.data.frame(fread("/z/Comp/lu_group/Members/nshen7/STAT628/Module2/Data/business_train.csv",header = T))
head(business)
business$categories = strsplit(business$categories,", ")
FindIndex <- function(string){ #find stores with "string" as category
  index = rep(0,nrow(business))
  for(i in 1:nrow(business)){
    if(string %in% business$categories[[i]]) index[i] = 1
  }
  return(index)
}
index.chn = FindIndex("Chinese")
sum(index.chn)
busID.chn = business$business_id[which(as.logical(index.chn))]
review.chn = review.cleaned[which(review.cleaned$bussiness_id%in%busID.chn),]
dim(review.chn)
head(review.chn)
write.csv(review.chn[,1:5],"/z/Comp/lu_group/Members/nshen7/STAT628/Module2/Data/review_train_chinese.csv",
          quote = T, row.names = F)
#draw wordclouds
library("wordcloud")
for(i in 1:5){
  words.star = review.chn$text.words[which(review.chn$stars==i)]
  words.star = unlist(words.star)
  words.star.count = table(words.star)
  sort(words.star.count,decreasing = T)[1:20]
  png(paste0("/z/Comp/lu_group/Members/nshen7/STAT628/Module2/Results/Plots/WordCloud_Chinese_star",i,".png"),height = 700,width = 700)
  set.seed(1234)
  wordcloud(words = rownames(words.star.count), freq = words.star.count, min.freq = 1,
            max.words=200, random.order=FALSE, rot.per=0.35, 
            colors=brewer.pal(8, "Dark2"))
  dev.off()
  print(i)
}


