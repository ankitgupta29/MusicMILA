from __future__ import division
from collections import defaultdict 
import re
import math
import pickle
from sklearn import svm
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier
from GenerateMoodTrainData import *
from GenerateActivityTrainData import *

def main():

	#X = [[0, 0], [1, 1]]
	#y = [0, 1]
	#X = pickle.load(open("SVM_train_MOOD_X_Feature_TF.txt","rb")) 
	#Y = pickle.load(open("SVM_train_MOOD_Y_ClassList.txt","rb"))
	#Z0 = pickle.load(open("SVM_test_MOOD_X_Feature_TF.txt","rb"))
	#Z1 = pickle.load(open("SVM_test_X_Feature_TF1.txt","rb"))
	#Z2 = pickle.load(open("SVM_test_X_Feature_TF2.txt","rb"))
	
	#print X.shape
	#clf = svm.SVC()
	#clf = LinearSVC(C=0.01, penalty="l1", dual=False).fit_transform(X,None)
	#print clf.shape

 	featMoodList,classMoodList = init_MoodTrain()
	featActList,classActList = init_ActTrain()
	print len(featMoodList) 
	print len(classMoodList)
	print len(featActList) 
	print len(classActList)
	
	moodClassifier = OneVsRestClassifier(LinearSVC(random_state=0)).fit(featMoodList,classMoodList)
	print "Mood Classification done"
	actClassifier = OneVsRestClassifier(LinearSVC(random_state=0)).fit(featActList,classActList)
	print "Training Done"
        while(1):
		print "Enter The Tweet"
		tweet = raw_input()
		print tweet
		testMV = createTestMoodFVec(tweet)
		testAV = createTestActFVec(tweet)	
		#print testV
		predM =  moodClassifier.predict(testMV)
		predA =  actClassifier.predict(testAV)
		print "Predicted Mood: ",mapClass2Mood(predM)
		print "Predicted Activity: ",mapClass2Act(predA)
		
	print "\nDone"
	return


if __name__ == '__main__':
    main()
