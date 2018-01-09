
import json
import csv
import pandas
import preprocessor as p

list_names=["Rape","Assault","Driving","Murder","Pickpocketing","Smuggling","Burglary"]
for name in list_names:
	tweets = []
	with open(name+'.json', 'r') as data_f:
		for line in data_f:
			data=json.loads(line)
			tweet = []
			if len(tweets) > 500 :
				break
			try:
				data['text']=p.clean(data['text'])
				tweet.append(data['text'].encode("utf-8"))
				tweet.append(name.encode("utf-8"))
				tweets.append(tweet)
			except:
				pass
	with open('people.csv', 'a') as f:
		writer = csv.writer(f)
		for i in tweets:
			writer.writerow(i)
   
		
 


