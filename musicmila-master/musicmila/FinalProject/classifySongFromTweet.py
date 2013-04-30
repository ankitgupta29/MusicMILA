import math
import pickle
from sklearn import svm
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier
from GenerateMoodTrainData import *
from GenerateActivityTrainData import *
from fetchTrackIdFromMILA import *
import sys,os
cd = os.getcwd()
new = cd + '/SongCollection/'
webpath = cd+'/static/'
sys.path.insert(0,new)

import hdf5_utils 
from get_preview_url import getURLFrom7D #getURLFromH5



featMoodList,classMoodList = init_MoodTrain()
featActList,classActList = init_ActTrain()
print len(featMoodList)
print len(classMoodList)
print len(featActList)
print len(classActList)
moodClassifier = OneVsRestClassifier(LinearSVC()).fit(featMoodList,classMoodList)
print "Mood Classification done"
actClassifier = OneVsRestClassifier(LinearSVC()).fit(featActList,classActList)
print "Training Done"
songClassDict = defaultdict()
songUrlList  = []


def classifySong(tweet):
	
	testMV = createTestMoodFVec(tweet)
	testAV = createTestActFVec(tweet)
        #print testV
        predM =  moodClassifier.predict(testMV)
        predA =  actClassifier.predict(testAV)
        mood  = mapClass2Mood(predM)
        activity = mapClass2Act(predA)
        print "Predicted Mood: ",mapClass2Mood(predM)
        print "Predicted Activity: ",mapClass2Act(predA)
	
        location = 'ohio'
	'''
         # hard coded 
        mood = "happy"
	activity = "chilling"	
	'''
	#hard code end
        songClassDict["Mood"] = mood
        songClassDict["Activity"] = activity

        songClassDict["Tweet"] = tweet
        songClassDict["Location"] = location
        songScoreDict,songTrackIdDId = fetchSong(mood,activity,location)
        json.dump(songClassDict,open(webpath+'tweet.json','wb'))
	songUrlList = []
        if(len(songScoreDict) > 0):
		sortedDict = sorted(songScoreDict.items(), key=lambda x: x[1],reverse = True)
		counter = 0
		for key in sortedDict:
			tup = songTrackIdDId[key[0]]
			digital_id = tup[0]
			songUrlDict = defaultdict()
			#key = 'TRAAABD128F429CF47'
			#key = key+ '.h5'

			URL = getURLFrom7D(digital_id)
			if URL is not None:
				#print URL
				#get the URL here
				songUrlDict["title"] = tup[1]
				songUrlDict['artist'] = tup[2]
				songUrlDict["mp3"] = URL
				songUrlList.append(songUrlDict)
				counter = counter+1
				#print "###### URL Dumped"
			else:
				print "***********  No url for this key **************"

			if (counter>10):
					break
	
		for key in songUrlDict:
			print key,songUrlDict[key]

		try:
   			with open('testsong.json'):
				os.remove(webpath + 'testsong.json')
		except IOError:
   			pass
                json.dump(songUrlList,open(webpath+'testsong.json','wb'))
        print "\nDone"




