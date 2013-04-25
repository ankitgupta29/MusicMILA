from guess_language import guess_language
import os,sys
import json as simplejson

def main():
				f = open('geo.2013-03-01_00-03.txt', "r")
				lines = f.readlines()
				i,no = 0,0
				txtfile = open('tweetdata.txt',mode ='wt')
				#csvout = csv.writer(open("tweet0.csv", "wb"))
				#csvout.writerow(["ID","place",'location',"coordinates","time_zone","hashtag","username","text","Mood1","Mood2","Activity1","Activity2"])
				for line in lines:	
								try:
												tweet = simplejson.loads(line)
												if "text" in tweet:
																text = str(tweet["text"].encode('utf-8','ignore'))
																
																language = guess_language(text)
																if language == 'en':
																				txtfile.write(line)
																				
															
													
								except ValueError:
												pass



if __name__ == '__main__':
 main()

