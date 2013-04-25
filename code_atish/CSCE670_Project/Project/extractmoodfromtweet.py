import requests
import os,json
from sys import argv
import shutil
import csv,re
import extractwordlist

cd = os.getcwd()
new = cd+'\\xlsfiles\\'
out  = cd + '\\output\\'
'''
if os.path.exists(out):
	shutil.rmtree(out)
os.mkdir(out)
'''
#myKey =  "EwSd72FSp9cCEVuWQVXnDO1TzU0"
myKey = "HUhepKdRcHCnvIb8uZRKB8m7d84"
start_url = "http://uclassify.com/browse/uClassify/Sentiment/ClassifyText?readkey=HUhepKdRcHCnvIb8uZRKB8m7d84&text="

myKey2 = "L4RIHrQpoCFQVClo905YujPJc"
start_url2 = "http://uclassify.com/browse/uClassify/Sentiment/ClassifyText?readkey=L4RIHrQpoCFQVClo905YujPJc&text="

myKey3 = "lsPGOC3fdPdJc2vqURS5boBOL7Y"
start_url3 = "http://uclassify.com/browse/uClassify/Sentiment/ClassifyText?readkey=lsPGOC3fdPdJc2vqURS5boBOL7Y&text="

end_url = "&output=json&version=0.01"

'''
def getResponse(url,user,auth,responseDict):
    r = requests.get(url,auth=(user,auth))
    
    #print r.status_code
    result =  r.json()
    #print result
    for j,i in enumerate(result['d']['results']):
        url = str(i['Url'].encode('utf-8','ignore'))
        title= str(i['Title'].encode('utf-8','ignore'))
        text = str(i['Description'].encode('utf-8','ignore'))
        doc = {}
        doc[url] = title+","+text
        responseDict.append(doc)
'''
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
	if pos > 0.5:	
		for word in wordList:
				if word in extractwordlist.happy:
					print "tweet [%s] ===change to happy===" %tweet
					mood = 'happy'
				if word in extractwordlist.love:
					print "tweet [%s] ===change to happy love===" %tweet
					mood = 'happy love'

	if neg >= 0.85:
		mood = "angry"
	if 0.5 < neg < 0.85:
		mood = 'sad'
	if neg > 0.6:		
		for word in wordList:
				if word in extractwordlist.love:
					print "tweet [%s] ===change to sad love===" %tweet
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
	bChangeKey = True
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
			fw = open(outfile ,'a')
			writer = csv.writer(fw)
			reader = csv.reader(f)
			for row in reader:
				text = fetchTextFromTweet(row)
				if(bChangeKey == True):
					url = start_url3 + text + end_url
					#print url	
					r = requests.get(url, auth=(myKey3, myKey3))
				else:	
					url = start_url + text + end_url
					print url	
					r = requests.get(url, auth=(myKey, myKey))
					#print r
					#print r.status_code
				if(r.status_code != 200):
					bChangeKey = True
				result = r.json()
				mood = fetchMoodFromRequest(result,row)
				row.append(mood)
				#finallist.append(row)
				#print finallist
				writer.writerow(row)
		'''
		#fw = open(outfile ,'a')
                #writer = csv.writer(fw)
		for row in finallist:
			writer.writerow(row)
		#print "Next file"
		'''
		
if __name__ == '__main__':
  main()		
		
