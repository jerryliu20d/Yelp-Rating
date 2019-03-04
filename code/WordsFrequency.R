#local codes
library(data.table)
options(stringsAsFactors=F)
review.chn = fread("/z/Comp/lu_group/Members/nshen7/STAT628/Module2/Data/review_train_chinese.csv")
review.chn$text.words = strsplit(review.chn$text,split = " ")
for(i in 1:5){ #barplots of word frequency in each rating category
  words.star = review.chn$text.words[which(review.chn$stars==i)]
  words.star = unlist(words.star)
  words.star.count = sort(table(words.star),decreasing = T)
  png(paste0("/Users/SX/Documents/AMERICA/STUDY/4th semester/STAT628/Module2/Results/Barplots/Barplot_WordsFreq_Star",i,".png"),width = 1000,height = 700)
  barplot(words.star.count[1:20],las=2)
  dev.off()
}

##====== Merge sentences back to whole review ======
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

#====== TF-IDF for each words from five ratings ======
FindCount <- function(word, text.list){ #find index of which review contains the "word"
  count = rep(0,length(text.list))
  for(i in 1:length(text.list)){
    count[i] = sum(text.list[i][[1]]==word, na.rm = T)
  }
  return(count)
}
sum(FindCount("good",review.sub$text))
sum(FindCount("best",review.sub$text))
FindLength <- function(text.list){ #find total number of terms in each review
  len = rep(0,length(text.list))
  for(i in 1:length(text.list)){
    len[i] = length(text.list[i][[1]])
  }
  return(len)
}
FindLength(review.sub$text[1:6])


freq_in_star <- function(word){ #take ratings as documents, calculate the TF-IDF of one word
  star = 1:5
  freq = rep(0,5)
  for(i in 1:5){
    dat = review.sub[which(review.sub$stars==i),]
    freq[i] = sum(FindCount(word,dat$text))/sum(FindLength(dat$text))
  }
  return(data.frame(star,freq))
}
dat = freq_in_star("best")
dat$star = as.factor(dat$star)
plot(dat)
chisq.test(x=dat$star,y=dat$freq)
summary(lm(star~freq, data = freq_in_star("good")))


