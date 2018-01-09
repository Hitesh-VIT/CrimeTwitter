
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.ensemble import AdaBoostClassifier 
from sklearn.svm import SVC
import numpy as np
import graphviz 
from sklearn import preprocessing
from sklearn.externals import joblib

filename = 'finalized_model.sav'
loaded_model = joblib.load(filename)
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.ensemble import AdaBoostClassifier 
from sklearn.svm import SVC
import numpy as np
import graphviz 
from sklearn import preprocessing
from sklearn.externals import joblib







tweets = pd.read_csv('tweets.csv')

f = pd.read_csv('people.csv', sep=',', names=['Text', 'Sentiment'], dtype=str, header=0)
le = preprocessing.LabelEncoder()
label= le.fit_transform(f['Sentiment'])
print le.classes_
 
	


def split_into_lemmas(tweet):
    bigram_vectorizer = CountVectorizer(ngram_range=(1, 3),stop_words='english', strip_accents='ascii', token_pattern=r'\b\w+\b', min_df=2)
    
    analyze = bigram_vectorizer.build_analyzer()
    
    return analyze(tweet)



bow_transformer = CountVectorizer(analyzer=split_into_lemmas, stop_words='english', strip_accents='ascii')
bow_transformer=bow_transformer.fit(f['Text'])
text_bow = bow_transformer.transform(f['Text'])

tfidf_transformer = TfidfTransformer().fit(text_bow)
tfidf = tfidf_transformer.transform(text_bow)

text_tfidf = tfidf_transformer.transform(text_bow)

from sklearn.model_selection import train_test_split


X_train, X_test, y_train, y_test = train_test_split( tfidf, label, test_size=0.33, random_state=42)


#classifier_nb = MultinomialNB(class_prior=None,fit_prior=False).fit(X_train, y_train)

#filename = 'finalized_model.sav'
#joblib.dump(classifier_nb, filename)

#score = classifier_nb.score(X_test,y_test)


#classifier_en = AdaBoostClassifier(n_estimators=100)
#classifier_en.fit(X_train, y_train)
#score2= classifier_en.score(X_test,y_test)
#print "Score for Naive--- "
#print score
#print "----"
#print score2


#classifier_svm=SVC(probability=True,kernel='sigmoid')
#classifier_svm.fit(text_tfidf,f['Sentiment'])
#score2 = classifier_svm.score(X_test,y_test)

#print "Score for AdaBoost Classifier with 100 estimators--- "
#print score2

sentiments = pd.DataFrame(columns=['text', 'class', 'prob'])






       
i = 0
for _, tweet in tweets.iterrows():
    i += 1
    try:
		
        bow_tweet = bow_transformer.transform(tweet)
        tfidf_tweet = tfidf_transformer.transform(bow_tweet)
        
        sentiments.loc[i-1, 'text'] = tweet.values[0]
        sentiments.loc[i-1, 'class'] = loaded_model.predict(tfidf_tweet)
        sentiments.loc[i-1, 'prob'] = round(loaded_model.predict_proba(tfidf_tweet)[0][1], 2)*10
        #sentiments.loc[i-1,'SVM']=classifier_svm.predict(tfidf_tweet)
        #sentiments.loc[i-1,'SVM_Prob']=round(classifier_svm.predict_proba(tfidf_tweet)[0][1], 2)*10

    except Exception as e:
        sentiments.loc[i-1, 'text'] = tweet.values[0]

sentiments.to_csv('sentiments.csv', encoding='utf-8')

print sentiments

