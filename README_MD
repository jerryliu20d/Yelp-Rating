This is about Yelp data analysis as a school project

Yelp data contains reviews of business and attributes of business and we decide to analyze Chinese restaurants. Our goal 1: tell a specific
Chinese restaurant how to improve their business and get a better rating on Yelp app. Our goal 2: predict the rating of a review based on 
the review and attributes of the business.

goal 1: we use light gbm to get feature importances and we test if it's significant and then we check if the Chinese restaurant have the 
best attribute. If it don't have the best attribute we will recommend the restaurant to make a change. Besides, we build five corpus of
differnt words and they stand for 'time, price, cleaness, food, service'. We calculate wasserstein distance to find which categorie is 
important. Then we calculate the mean of stars of bad(one or two stars) reviews and good(four or five stars) reviews for each of five
categories and it will tell us whether the restaurant have a good performance on a specific category and then we can give some advise to 
the restaurants.

goal 2: we tokenize the text and then build a neural network. The neural network contains embedding layer,lstm layer, poolling layer,
dropout layer and dense layer and we cutoff ratings if they are below 1 or above 5.

todo: the corpus of each category is not precise and wasserstein distance may not be a good measure method for the difference of two 
distributions. And we can try to deal with missing data in different ways.

