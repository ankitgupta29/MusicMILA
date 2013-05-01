
from __future__ import division
from collections import defaultdict 
import re,json
import math
import pickle
from sklearn import svm
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier
from GenerateMoodTrainData import *
from GenerateActivityTrainData import *
from fetchTrackIdFromMILA import *

#from classifySongFromTweet import *
def computeMicroAvg(preRecAvgDict):
    totalTP = 0
    totalFP = 0
    totalFN = 0
    for classType in preRecAvgDict:
        #print classType
        totalTP = totalTP+preRecAvgDict[classType][0]
        totalFP = totalFP+preRecAvgDict[classType][1]
        totalFN = totalFN+preRecAvgDict[classType][2]
    precission = totalTP/(totalTP+totalFP)
    print "True Positives [%d]" %totalTP
    print "False Positives [%d]" %totalFP
    print "False Negatives [%d]" %totalFN
    
    print "precission[%s]" %precission
    recall = totalTP/(totalTP+totalFN)
    print "recall [%s]" %recall
    microAvg = 2*precission*recall/(precission+recall)
    print "Micro Avg F1 Value = ",microAvg
    return

def main():

	#X = [[0,0],[1,1],[0,1],[1,0]]
	#Y = [0,1,1,0]
	#X = [[0,0],[1,1]]
	#Y = [0,1]
	#Z0 = [0,1]
	#Z1 = [1]
	X = pickle.load(open("SVM_train_MOOD_X_Feature_TF.txt","rb")) 
	Y = pickle.load(open("SVM_train_MOOD_Y_ClassList.txt","rb"))
	Z0 = pickle.load(open("SVM_test_MOOD_X_Feature_TF.txt","rb"))
	Z1 = pickle.load(open("SVM_test_MOOD_Y_ClassList.txt","rb"))
	'''
 	featMoodList,classMoodList = init_MoodTrain()
	featActList,classActList = init_ActTrain()
	
	'''
 	featMoodList,classMoodList = X,Y
	#featActList,classActList = init_ActTrain()
	print len(featMoodList) 
	print len(classMoodList)
	#print len(featActList) 
	#print len(classActList)
	
	moodClassifier = OneVsRestClassifier(LinearSVC(random_state=0)).fit(featMoodList,classMoodList)
	print "Mood Classification done"
	#actClassifier = OneVsRestClassifier(LinearSVC(random_state=0)).fit(featActList,classActList)
	print "Training Done"
	testMV = Z0
	#print testMV
	predM =  moodClassifier.predict(testMV)
	#print predM
        print "Mood Classification Done"
        preRecAvgDict = defaultdict(list) # {classType:[TP,FP,FN,TN]}		
	numMood = 5
	for mood in range(numMood):
		print mood
		preRecAvgDict[mapMood2Class(mood)].append(0)
       	 	preRecAvgDict[mapMood2Class(mood)].append(0)
        	preRecAvgDict[mapMood2Class(mood)].append(0)	
	
	truePos = 0
        falsePos = 0
        falseNeg = 0
        for cIndex,clMood in enumerate(predM):
		print clMood
		print Z1[cIndex]
		if( clMood == Z1[cIndex]):
			
			#truePos = truePos+1
        		preRecAvgDict[mapMood2Class(clMood)][0] =   preRecAvgDict[mapMood2Class(clMood)][0] +1
       		elif(clMood != Z1[cIndex]):
			#falseNeg = falseNeg+1
        		preRecAvgDict[mapMood2Class(clMood)][2] =   preRecAvgDict[mapMood2Class(clMood)][2]+1 
		preRecAvgDict[mapMood2Class(clMood)][1] = preRecAvgDict[mapMood2Class(clMood)][1]+1
        print preRecAvgDict
    	microAvg = computeMicroAvg(preRecAvgDict)    	
	'''
	songClassDict = defaultdict()
	songUrlDict   = defaultdict(list)
	
	while(1):
		print "Enter The Tweet"
		tweet = raw_input()
		print tweet
		classifySong(tweet)
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
				#get the URL here
				songUrlDict["URL"].append(key[0])
				if (counter>10):
					break
				counter = counter+1
					
		else:
			print "Empty Song List :("
		
		json.dump(songUrlDict,open('tweetSongUrl.json','wb'))
	print "\nDone"
	'''
	return


if __name__ == '__main__':
    main()
