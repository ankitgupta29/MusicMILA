import sys
import simplejson
import difflib
from collections import defaultdict
import re,os,simplejson,csv



class Tweet():
	def __init__(self):
		self.id = None
		self.place = None
		self.text = None
		self.location = None
		self.time_zone = None
		self.coordinates = None
		self.hashtag = None
		self.username = None

	def loadtweet(self,tweet):

		self.id = tweet["id"]
		self.text = tweet["text"].lower()
		user = tweet['user']
                self.username = str(user["screen_name"]).lower()
		self.location = str(user["location"]).lower()
		self.time_zone = str(user["time_zone"]).lower()

		
		place = tweet['place']
		city,country = '',''
		if place:
			city = str(place['full_name']).lower()
			country = str(place['country']).lower()
		self.place = (city,country)
		
		geo = tweet['geo']
		if geo:
			self.coordinates = str(geo['coordinates'])
			
		
		entities = tweet["entities"]
		hashtaglist = []
		if entities:
			taglist = []
			hashtaglist = entities.get("hashtags")
			if not len(hashtaglist) == 0:
				for item in hashtaglist:
					tag = str(item['text']).lower()		
					taglist.append(tag)
				self.hashtag = taglist

	def tprint(self):
		print "ID   	         : %s" %self.id
		print "place             : %s,%s" %(self.place[0],self.place[1])
                print "text              : %s" %self.text
                print "location          : %s" %self.location
                print "time_zone         : %s" %self.time_zone
                print "coordinates       : %s" %self.coordinates
                print "hashtag           : %s" %self.hashtag
                print "username          : %s" %self.username


def FeedDataFromTweet(t):
	infolist = [t.id,t.place,t.location,t.coordinates,t.time_zone,t.hashtag,t.username,t.text]
	return infolist

def main():
	
        f = file('tweetdata.txt', "r")
        lines = f.readlines()
	i,no = 0,0
	csvout = csv.writer(open("/home/ankit/IRProject/xlsfiles/tweet0.csv", "wb"))
	csvout.writerow(["ID","place",'location',"coordinates","time_zone","hashtag","username","text","Mood1","Mood2","Activity1","Activity2"])
        for line in lines:
		
                try:
			if not "{\"limit\":{\"track\":" in line:
                        	tweet = simplejson.loads(unicode(line),encoding="UTF-8")
				list1 = []
				tweetObject = Tweet()
				tweetObject.loadtweet(tweet)
				i = i +1
				if i > 2000:
					#print "I is :",i
					no = no + 1
					i = 0
					filename = "/home/ankit/IRProject/xlsfiles/" + "tweet" + str(no) + ".csv"
					csvout = csv.writer(open(filename, "wb"))
				csvout.writerow(FeedDataFromTweet(tweetObject))	
		
		except ValueError:
			pass
		#print "==========================================================\n"


if __name__ == '__main__':
 main()

