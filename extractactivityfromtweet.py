import requests0 as requests
import os,json
from sys import argv
import shutil
import csv,re
import extractwordlist
import operator

cd = os.getcwd()
new = cd+'/xlsfiles/'
out  = cd + '/ActivityMoodFiles/'


def fetchActivityFromTweet(row):
	physical,mental,daily,relaxing,chilling = 0,0,0,0,0
	tweet = row[-2]  #fetch text at last column
        wordList = re.sub("[^\w]", " ",  tweet).split()
	countlist = [0,0,0,0,0]
	for word in wordList:

        	if word in extractwordlist.physical:
			countlist[0] = countlist[0] + 1
		if word in extractwordlist.mental:
			countlist[1] = countlist[1] + 1
		if word in extractwordlist.daily:
			countlist[2] = countlist[2] + 1
		if word in extractwordlist.chilling:
			countlist[3] = countlist[3] + 1
		if word in extractwordlist.relaxing:
			countlist[4] = countlist[4] + 1
	index, value = max(enumerate(countlist), key=operator.itemgetter(1))
	if value == 0:
		return "Neutral"

	if index == 0:
		return 'physical'

        if index == 1:
                return 'mental'

        if index == 2:
                return 'daily'

        if index == 3:
                return 'chilling'

        if index == 4:
                return 'relaxing'




def fetchTextFromTweet(row):
	isfirst = True
        tweet = row[-2] #fetch text at last column
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
		if "~lock" not in files:
			f = open(files, 'r')
			outfile = "out" + files
			os.chdir(out)
			fw = open(outfile ,'a')
			writer = csv.writer(fw)
			reader = csv.reader(f)
			for row in reader:
				activity = fetchActivityFromTweet(row)
				if activity != 'Neutral':
					'''
					print row[-2]
					print activity
					print '======================'
					'''
					row.append(activity)
				writer.writerow(row)
		
if __name__ == '__main__':
  main()		
		
