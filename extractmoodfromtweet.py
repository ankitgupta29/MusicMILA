import requests0 as requests
import os,json
from sys import argv
import shutil
import csv,re
import extractwordlist

cd = os.getcwd()
new = cd+'/xlsfiles/'
out  = cd + '/output/'

if os.path.exists(out):
	shutil.rmtree(out)
os.mkdir(out)

#myKey =  "EwSd72FSp9cCEVuWQVXnDO1TzU0"
myKey = "No5zUHJPDt7xAro9hJU4f0VR0"
start_url = "http://uclassify.com/browse/uClassify/Sentiment/ClassifyText?readkey=No5zUHJPDt7xAro9hJU4f0VR0&text="
end_url = "&output=json&version=0.01"


def fetchMoodFromRequest(r,row):
	tweet = row[-1] #fetch text at last column
        wordList = re.sub("[^\w]", " ",  tweet).split()
	pos = r['cls1']['positive']
        neg = r['cls1']['negative']

	#print wordList
	#print "pos,neg = ",pos,neg
	mood  = None

        if pos >= 0.75:
                mood = "happy"
	
        if 0.5 <= pos < 0.75:
		mood = 'calm'
		for word in wordList:
			if word in extractwordlist.happy:
				#print "================change to happy========================="
                		mood = 'happy'
			if word in extractwordlist.love:
				#print "==================change to happy love======================="
				mood = 'happy love'

        if neg >= 0.85:
                mood = "angry"

        if 0.5 < neg < 0.85:
		mood = 'sad'
		for word in wordList:
			if word in extractwordlist.angry:
				#print "========change to angry========"
        	        	mood = "angry"
			if word in extractwordlist.love:
				#print "==========change to sad love============="
				mood = 'sad love'
	#print mood
        return mood


def fetchTextFromTweet(row):
	isfirst = True
        tweet = row[-1] #fetch text at last column
        wordList = re.sub("[^\w]", " ",  tweet).split()
        text = ''
      	for word in wordList:
        	if isfirst:
                	text = word
                        isfirst = False
                else:
                        text = text + "+" + word
	return text


def main():
	os.chdir(new)
	listing =  os.listdir(new)
	for files in listing:
		finallist = []
		os.chdir(new)
		#print files
		if "~lock" not in files:
			f = open(files, 'r')
			outfile = "out" + files
			os.chdir(out)
			#fw = open(outfile ,'a')
			#writer = csv.writer(fw)
			reader = csv.reader(f)
			for row in reader:
				text = fetchTextFromTweet(row)
				url = start_url + text + end_url	
		    		r = requests.get(url, auth=(myKey, myKey)).json
				mood = fetchMoodFromRequest(r,row)
				row.append(mood)
				finallist.append(row)
				#writer.writerow(row)
		#fw = open(outfile ,'a')
                #writer = csv.writer(fw)
		for row in finallist:
			writer.writerow(row)
		#print "Next file"
		
if __name__ == '__main__':
  main()		
		
