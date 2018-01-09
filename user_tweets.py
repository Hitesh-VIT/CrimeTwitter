#!/usr/bin/env python
# encoding: utf-8

import tweepy
import csv




access_key = "907636142987558914-NXtnukVQoL8OqkbCQg0xgMhbx7z48NY"
access_secret = "NVoOzE69pn17DFW996KAuHsqisyStsRshOREgL004qUjB"
consumer_key = "9fi7SGkNTmJ7aB0mAqk2MnD32"
consumer_secret = "rQWLQ5DDiYuRjELtYF521G6LQqQzKQpkR7jjF8tu5PMa7c5g3I"

def get_all_tweets(screen_name):
	
	
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	

	alltweets = []	
	
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
	alltweets.extend(new_tweets)
	
	oldest = alltweets[-1].id 
	
	
	while len(new_tweets) > 0:
		print "getting tweets before %s" % (oldest)
		
		
		
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		
		alltweets.extend(new_tweets)
		
		
		oldest = alltweets[-1].id - 1
		print "...%s tweets downloaded so far" % (len(alltweets))
		
			
	
	outtweets = [ tweet.text.encode("utf-8") for tweet in alltweets]
	
		
	with open('%s_tweets.csv' % screen_name, 'wb') as f:
		writer = csv.writer(f,delimiter=',',)
		writer.writerow(["tweets"])
		writer.writerow(outtweets)
	
	pass


if __name__ == '__main__':
	screen_name = raw_input("Enter the user name")
	get_all_tweets(screen_name)

