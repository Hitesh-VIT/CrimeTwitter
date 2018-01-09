
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import pymongo
from pymongo import MongoClient
import json
from ast import literal_eval

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
from threading import Thread


def split_into_lemmas(tweet):
	bigram_vectorizer = CountVectorizer(ngram_range=(1, 3),stop_words='english', strip_accents='ascii', token_pattern=r'\b\w+\b', min_df=2)
	
	analyze = bigram_vectorizer.build_analyzer()
	
	return analyze(tweet)


f = pd.read_csv('people.csv', sep=',', names=['Text', 'Sentiment'], dtype=str, header=0)
bow_transformer = CountVectorizer(analyzer=split_into_lemmas, stop_words='english', strip_accents='ascii')


bow_transformer=bow_transformer.fit(f['Text'].values.astype('U'))
text_bow = bow_transformer.transform(f['Text'].values.astype('U'))

tfidf_transformer = TfidfTransformer().fit(text_bow)
tfidf = tfidf_transformer.transform(text_bow)




client = MongoClient('localhost', 27017)
db = client.test_database
posts = db.posts



access_token = "907636142987558914-NXtnukVQoL8OqkbCQg0xgMhbx7z48NY"
access_token_secret = "NVoOzE69pn17DFW996KAuHsqisyStsRshOREgL004qUjB"
consumer_key = "9fi7SGkNTmJ7aB0mAqk2MnD32"
consumer_secret = "rQWLQ5DDiYuRjELtYF521G6LQqQzKQpkR7jjF8tu5PMa7c5g3I"


filename = 'finalized_model.sav'
loaded_model = joblib.load(filename)




class StdOutListener(StreamListener):
	
	def __init__(self,handle):
		self.handle = handle

	def on_data(self, data):
		try:
			
		
				context={}
				all_data=json.loads(data)
				
				tweet = [all_data['text'].encode('utf-8')]
				
				
				bow_tweet = bow_transformer.transform(tweet)
				tfidf_tweet = tfidf_transformer.transform(bow_tweet)
				
				context['location']=self.handle
				print "---"
				crime=loaded_model.predict(tfidf_tweet)
				if crime[0] == 0 :
					context['crime']='Assault'
				elif crime[0] == 1 :
					context['crime']='Burglary'
				elif crime[0] == 2 :
					context['crime']='Driving'
				elif crime[0] == 3 :
					context['crime']='Murder'
				elif crime[0] == 4 :
					context['crime']='Pickpocketing'
				elif crime[0] == 5 :
					context['crime']='Rape'
				elif crime[0] == 6 :
					context['crime']='Smuggling'
				
				context['text'] = all_data['text'] 
				
					
					
				
				
				post_id=posts.insert(context)
				return True
		except BaseException as e:
			print("Error on_data: %s" % str(e))
		return True
		

	def on_error(self, status):
		print status


def stream_twitter(handle,geobox):
	l = StdOutListener(handle)
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	stream = Stream(auth, l)
	stream.filter(locations=geobox,async=True)



if __name__ == '__main__':

	
	#t1=Thread(target=stream_twitter, args=("Ireland", [-30.5,58.9,-1.1,69.6]))
	#t2=Thread(target=stream_twitter, args=("Cuba", [-83.5,14.8,-64.2,27.2]))
	t3=Thread(target=stream_twitter, args=("Cape Town", [16.95,-35.75,23.48,-30.07]))
	#t4=Thread(target=stream_twitter, args=("New York", [-78.37,39.41,-70.69,42.77]))
	t5=Thread(target=stream_twitter, args=("Toronto", [-83.19,41.97,-73.79,48.04]))
	
	
	
	
	#t1.start()
	#t2.start()
	t3.start()
	#t4.start()
	t5.start()
	



"""


	Assassination Assault Battery Bigamy Criminal negligence False imprisonment Home invasion Homicide Kidnapping Manslaughter (corporate) Mayhem Murder
		corporate Negligent homicide Public indecency Rape Robbery Sexual assault 

Crimes against property

	Arson Blackmail Bribery Burglary Embezzlement Extortion False pretenses Fraud Larceny Payola Pickpocketing Possessing stolen property Robbery Smuggling Tax evasion Theft 
"""
