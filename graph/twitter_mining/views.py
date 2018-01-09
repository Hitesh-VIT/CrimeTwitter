# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import sys
import requests
import json
import twitter
import config
import networkx as nx

import sys
import requests
import json
import twitter
import config
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import pymongo
from pymongo import MongoClient
from fbprophet import Prophet
import numpy as np
import pandas as pd
import datetime


start = '01MAY2017 11:45'
start_date = datetime.datetime.strptime(start, '%d%b%Y %H:%M').date()

client = MongoClient('localhost', 27017)
db = client.test_database
posts = db.posts
location= ["Mumbai".encode('utf-8'),"Delhi".encode('utf-8'),"Chennai".encode('utf-8'),"Kolkata".encode('utf-8'),"London".encode('utf-8'),"Washington DC".encode('utf-8'),"Hague".encode('utf-8'),"New York".encode('utf-8'),"Chicago".encode('utf-8'),"Cuba".encode("utf-8")]

@csrf_exempt
def twitter_name(request):
	return render(request,'index.html',{})


@csrf_exempt
def twitter_name_chart(request):
	list_names=["Rape".encode('utf-8'),"Assault".encode('utf-8'),"Driving".encode('utf-8'),"Murder".encode('utf-8'),"Pickpocketing".encode('utf-8'),"Smuggling".encode('utf-8'),"Burglary".encode('utf-8')]
	percentage=[]
	if request.method == 'POST' :
		handle=request.POST['handle']
		for i in list_names :
			percentage.append(int(posts.find({"location":handle,"crime":i}).count()))
		return render(request,'chart.html',{"name":list_names,"percentage":percentage,'user':handle})
	else :
		return render(request,'chart.html',{})


def twitter_crime_chart(request):
	percentage=[]
	if request.method == 'POST' :
		handle=request.POST['handle']
		for i in location :
			percentage.append(int(posts.find({"location":i,"crime":handle}).count()))

		return render(request,'chart-crime.html',{"name":location,"percentage":percentage,'user':handle})
	else :
		return render(request,'index.html',{})






@csrf_exempt
def twitter_name_user(request):
	name=[]
	percentage=[]
	if request.method == 'POST' :
		handle=request.POST['handle']
		percentage,name=get_tweet_array(handle)
		thrill_value = [name[0],name[5],name[12],name[14],name[24]]
		average_thrill = (sum(thrill_value)/len(thrill_value))*100
		thrill_label = [percentage[0],percentage[5],percentage[12],percentage[14],percentage[24]]
		emotional_value = [name[2],name[1],name[4],name[8],name[9],name[10],name[11],name[14],name[25],name[26]]
		average_emotional = (sum(emotional_value)/len(emotional_value))*100
		emotional_label = [percentage[2],percentage[1],percentage[4],percentage[8],percentage[9],percentage[10],percentage[11],percentage[14],percentage[25],percentage[26]]





		data = {"thrill":average_thrill,"emotional":average_emotional,'name':percentage,'percentage':name,'user':handle,'thrill_value':thrill_value,"thrill_label":thrill_label,"emotional_value":emotional_value,"emotional_label":emotional_label}


		return render(request,'chart_2.html',data)
	else :
		return render(request,'user_data.html',{})


@csrf_exempt
def twitter_name_list(request):
	if request.method == 'POST' :
		location1 = request.POST['handle']
		crime = request.POST['crime']
		obj=posts.find({"location":location1,"crime":crime})
		obj=list(obj)
		return render(request,'tweet-list.html',{"list":obj})
	else :
		return render(request,'tweet.html',{})


@csrf_exempt
def twitter_city_list(request):
	if request.method == 'GET' :
		crime=["Rape".encode('utf-8'),"Assault".encode('utf-8'),"Driving".encode('utf-8'),"Murder".encode('utf-8'),"Pickpocketing".encode('utf-8'),"Smuggling".encode('utf-8'),"Burglary".encode('utf-8')]
		data=[]
		for i in location :
			value=[]
			for j in crime:
				
				value.append((int(posts.find({"location":i,"crime":j}).count())))

			data.append(value)
		main_data=zip(location,data)

		
		return render(request,'city.html',{"data":data,"crime":crime,'location':location,"main":main_data})
	else :
		return render(request,'city.html',{"data":data,"crime":crime})






@csrf_exempt
def twitter_crime_list(request):
	if request.method == 'GET' :
		crime=["Rape".encode('utf-8'),"Assault".encode('utf-8'),"Driving".encode('utf-8'),"Murder".encode('utf-8'),"Pickpocketing".encode('utf-8'),"Smuggling".encode('utf-8'),"Burglary".encode('utf-8')]
		data=[]
		for i in crime :
			value=[]
			for j in location:
				
				value.append((int(posts.find({"location":j,"crime":i}).count())))

			data.append(value)
		main_data=zip(crime,data)
		return render(request,'crime.html',{"data":data,"crime":crime,'location':location,"main":main_data})
	else :
		return render(request,'crime.html',{"data":data,"crime":crime})










def convert_status_to_pi_content_item(s):
    # My code here
    return {
        'userid': str(s.user.id),
        'id': str(s.id),
        'sourceid': 'python-twitter',
        'contenttype': 'text/plain',
        'language': s.lang,
        'content': s.text,
        'created': s.created_at_in_seconds,
        'reply': (s.in_reply_to_status_id == None),
        'forward': False
    }

def get_tweet_array(handle):
	handle = handle
	
	twitter_api = twitter.Api(consumer_key=config.twitter_consumer_key,
	                          consumer_secret=config.twitter_consumer_secret,
	                          access_token_key=config.twitter_access_token,
	                          access_token_secret=config.twitter_access_secret,
	                          debugHTTP=False)
	
	max_id = None
	statuses = []
	for x in range(0, 16):  # Pulls max number of tweets from an account
	    if x == 0:
	        statuses_portion = twitter_api.GetUserTimeline(screen_name=handle,
	                                                       count=200,
	                                                       include_rts=False)
	        status_count = len(statuses_portion)
	        max_id = statuses_portion[status_count - 1].id   # get id of last tweet and bump below for next tweet set
	    else:
	        statuses_portion = twitter_api.GetUserTimeline(screen_name=handle,
	                                                       count=200,
	                                                       max_id=max_id,
	                                                       include_rts=False)
	        status_count = len(statuses_portion)
	        max_id = statuses_portion[status_count - 1].id   # get id of last tweet and bump below for next tweet set
	    for status in statuses_portion:
	        statuses.append(status)
	
	pi_content_items_array = map(convert_status_to_pi_content_item, statuses)
	pi_content_items = {'contentItems': pi_content_items_array}
	
	r = requests.post(config.pi_url + '/v2/profile',
	                  auth=(config.pi_username, config.pi_password),
	                  headers={
	                      'content-type': 'application/json',
	                      'accept': 'application/json'
	                  },
	                  data=json.dumps(pi_content_items)
	                  )
	
	
	
	text=json.loads(r.text)
	
	
	
	
	name=[]
	value=[]
	
	for i in text['tree']['children']:
	    for j in i['children']:
			if j['children']:
				for m in j['children']:
					try:
						for n in m['children']:
							if n['name'] == 'Sunday' or n['name']=='0:00 am' :
								break
							name.append(str(n['name']).encode("utf-8"))
							value.append((n['percentage']))
					except:
						pass	 				 
	return (name,value)


	
	
def time_series(request):
	sales_df = pd.read_csv('sales.csv')
	sales_df['y_orig'] = sales_df['y']  

	sales_df['y'] = np.log(sales_df['y'])
	model = Prophet() 
	model.fit(sales_df); 
	future_data = model.make_future_dataframe(periods=6, freq = 'm')
	forecast_data = model.predict(future_data)
	s=pd.DatetimeIndex(forecast_data['ds']).date
	l=list(s)
	final=[]
	for i in l:
		j=i.strftime('%m/%d/%Y').encode("utf-8")
		final.append(j)
	return render(request ,'time.html',{"date":final,"data":list(forecast_data["yhat"])})


		
	
	


		
	


