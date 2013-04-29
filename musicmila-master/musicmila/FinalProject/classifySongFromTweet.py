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
sys.path.insert(0,new)

import hdf5_utils 
from get_preview_url import getURLFromH5


featMoodList,classMoodList = init_MoodTrain()
featActList,classActList = init_ActTrain()
print len(featMoodList)
print len(classMoodList)
print len(featActList)
print len(classActList)
#moodClassifier = OneVsRestClassifier(LinearSVC(random_state=0)).fit(featMoodList,classMoodList)
print "Mood Classification done"
#actClassifier = OneVsRestClassifier(LinearSVC(random_state=0)).fit(featActList,classActList)
print "Training Done"
songClassDict = defaultdict()
songUrlDict   = defaultdict(list)


def classifySong(tweet):
	'''
	testMV = createTestMoodFVec(tweet)
	testAV = createTestActFVec(tweet)
        #print testV
        predM =  moodClassifier.predict(testMV)
        predA =  actClassifier.predict(testAV)
        mood  = mapClass2Mood(predM)
        activity = mapClass2Act(predA)
        print "Predicted Mood: ",mapClass2Mood(predM)
        print "Predicted Activity: ",mapClass2Act(predA)
	'''
        location = 'ohio'
	
         # hard coded 
        mood = "happy"
	activity = "chilling"	
	#hard code end
        songClassDict["Mood"] = mood
        songClassDict["Activity"] = activity

        songClassDict["Tweet"] = tweet
        songClassDict["Location"] = location
        songScoreDict = fetchSong(mood,activity,location)
        json.dump(songClassDict,open('tweetMILA.json','wb'))

        if(len(songScoreDict) > 0):
		sortedDict = sorted(songScoreDict.items(), key=lambda x: x[1],reverse = True)
		counter = 0
		for key in sortedDict:
                                print key
				key = 'TRAAABD128F429CF47'
				key = key+ '.h5'
				
				URL = getURLFromH5(key)
				if URL is not None:
					print URL
                                	#get the URL here
                                	songUrlDict["URL"].append(key[0])
                                	counter = counter+1
				else:
					print "No url for this key"
				
                                if (counter>10):
                                        break
                else:
                        print "Empty Song List :("

                json.dump(songUrlDict,open('tweetSongUrl.json','wb'))
        print "\nDone"




