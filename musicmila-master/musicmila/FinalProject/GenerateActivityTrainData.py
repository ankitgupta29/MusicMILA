'''
	locationlist = (location_input.lower()).split()
Created on Apr 20, 2013

@author: Atish K Patra
This Class generates the training data set for MusicMILA suitable for sci-kit SVM Learn
'''
from __future__ import division
from collections import defaultdict
import re,os
import math
import pickle
import csv,re
from collections import defaultdict
#global Term Set
termSet = set()
actTermSet = set()
class TDProp:
    TD_ID       = 1;
    TD_PLACE    = 2;
    TD_COORD    = 3;
    TD_TZ       = 4; #TIME ZONE
    TD_HASHTAG  = 5;
    TD_UNAME    = 6;
    TD_TEXT     = 7;
    TD_MOOD1    = 8;
    TD_ACT1     = 9;
 
# 0 does not belong to any class        

class ACTList:
    ACT_DAILY = 1;
    ACT_CHILLING = 2;
    ACT_PHYSICAL = 3;
    ACT_RELAX = 4;
    ACT_MENTAL = 5;

def getBasePath():
    if os.name == 'nt': # Windows
        basePath = '\\'
    else:
        basePath = '/'
    #print basePath
    return basePath
   
    
def createTFdict(doc,bTrain,stopWordList):
    tfdict = defaultdict()
    #termList = [p for p in doc.lower().split() for p in re.findall(r"[\w]+",p)]
    tList = doc.lower().split()
    for tIndex,term in enumerate(tList):
        #print term
        if "@" in term :
            #print "Deleted Term",term
            del tList[tIndex]
    termList = [p for p in tList  for p in re.findall(r"['\&\-\.\/()=:;,_^ ->\]\[]+",p)]
    
    for tIndex,term in enumerate(termList):
        #print term
        if (len(term) <2) or (term in stopWordList) :
            #print "Deleted Term",term
            del termList[tIndex]
    smileyList = [p for p in tList for p in re.findall(r"[\w]+",p)]
    #print termList
    for fterm in termList:
        if fterm in tfdict :
            tfdict[fterm] = tfdict[fterm]+1
        else:
            tfdict[fterm] = 1
        if(bTrain):
            termSet.add(fterm)
    for sm in smileyList:
        if sm in tfdict :
            tfdict[sm] = tfdict[sm]+2
        else:
            tfdict[sm] = 2
        if(bTrain):
            termSet.add(sm)
    return tfdict

def addSmileyFeatures():
    numTotalSmiley = 0
    smileyDirPath = os.getcwd()+getBasePath()+"smiley"+getBasePath()
    fileList =  os.listdir(smileyDirPath)
    print "Smiley List files from",smileyDirPath
    for file in fileList:
        smList = open(smileyDirPath+file,'r').read().split()
        numTotalSmiley = numTotalSmiley+len(smList)
        for sm in smList:
            termSet.add(sm)
    return numTotalSmiley

def addActivityFeatures():
    numTotalSmiley = 0
    actDirPath = os.getcwd()+getBasePath()+"wordlists"+getBasePath()+"activity"+getBasePath()
    print "Activity WordList files from",actDirPath
    fileList =  os.listdir(actDirPath)
    for file in fileList:
        #print file
        acList = open(actDirPath+file,'r').read().split()
        #print acList
        for ac in acList:
            termSet.add(ac)
    return

def createStopWList():
    stopWDPath = os.getcwd()+getBasePath()+"en.txt"
    print "Stop WordList files from",stopWDPath

    stopWordList = open(stopWDPath,'r').read()
    #print stopWordList
    return stopWordList

def getFeatureVector(totalNumDocs,tfFeatureList,tfDictList):
    #print totalNumDocs,len(tfFeatureList),len(tfDictList)
    #print len(termSet)
    for x in range(totalNumDocs):
        zeroList = [0 for x in range(len(termSet))]
        #print dIndex
        tfFeatureList.append(zeroList)
    print len(tfFeatureList[0])
    for tIndex,term in enumerate(termSet):
        #print term,tIndex
        for dIndex,eachDocDict in enumerate(tfDictList):
            if term in eachDocDict:
                docfList = tfFeatureList[dIndex]   
                docfList[tIndex] = eachDocDict[term]
                #print "Term[%s] DIndex = [%s] [%s]"%(term,dIndex,tIndex)
    print "~~~~~~~~ Term FeatureList Created~~~~~~~~~~~"  
    
    return tfFeatureList


def mapClass2Act(actClassNum):
    actClass = ""
    if actClassNum == ACTList.ACT_MENTAL:
        actClass = "Mental Acitivity"
    elif actClassNum == ACTList.ACT_CHILLING:
        actClass = "Chilling"
    elif actClassNum == ACTList.ACT_RELAX:
        actClass = "Relaxing"
    elif actClassNum == ACTList.ACT_PHYSICAL:
        actClass = "Physical Activity"
    elif actClassNum == ACTList.ACT_DAILY:
        actClass = "Routine Activity"
    return actClass    

def mapActivity2Class(actType):
    actClassNum = -1
    if actType == "mental":
        actClassNum = ACTList.ACT_MENTAL
    elif actType == "chilling":
        actClassNum = ACTList.ACT_CHILLING
    elif actType == "relaxing":
        actClassNum = ACTList.ACT_RELAX
    elif actType == "physical":
        actClassNum = ACTList.ACT_PHYSICAL
    elif actType == "daily":
        actClassNum = ACTList.ACT_DAILY
    return actClassNum

def readallTweets(path):
    filList =  os.listdir(path)
    classActList = []
    docActList = []
    for file in filList:
        print file
        reader = csv.reader(open(path+file,'r'))
        totalRowLen = 0;
        for rIndex,row in enumerate(reader):
            #print row[TDProp.TD_TEXT] //Text
            totalRowLen = totalRowLen+1
            #print rIndex,len(row)
            if(rIndex > 0):
                #print rIndex,row[TDProp.TD_ACT1] #//Mood1
                if(len(row)==TDProp.TD_ACT1+1):
                    #print "Row Len",len(row)
                    #print rIndex,row[TDProp.TD_ACT1]
                    classActList.append(mapActivity2Class(row[TDProp.TD_ACT1]))
                    docActList.append(row[TDProp.TD_TEXT])
        #print classActList
        #print "NumRows",totalRowLen
        
    return classActList,docActList

def dumpTfFeatureList(docList,bTrain,stopWordList):
    tfFeatureList = []
    tfDictList = []
    tfDocList = []
    totallen = 0
    for dIndex,doc in enumerate(docList):
        tfDict = createTFdict(doc,bTrain,stopWordList)
        #print tfDict
        tfDictList.append(tfDict)
        #print termSet, len(tfDictList)
    totalNumDocs = len(docList)
    if bTrain:
        print "Trianing Data Formatting is Done TOtal Terms [%s]" %(len(termSet))
    else:
        print "Test Data Formatting is Done TOtal Terms [%s]" %(len(termSet))

    print "Total Documents in Corpus [%s]" %totalNumDocs
    tfFeatureList = getFeatureVector(totalNumDocs,tfFeatureList,tfDictList)                 
    return tfFeatureList

def createTestActFVec(text):
    dummyList = []
    dummyList.append(text)
    #tfFeatureList,classMoodList,classActList = init() 
    stopWordList = createStopWList()
    featureTList = dumpTfFeatureList(dummyList,False,stopWordList)
    return featureTList

def init_ActTrain():

    stopWordList = createStopWList()
    addSmileyFeatures()
    addActivityFeatures()
    print "~~~~~~Begin Creating the dataset~~~~~~~~"
    trainDPath = os.getcwd()+getBasePath()+"train"+getBasePath()
    testDPath = os.getcwd()+getBasePath()+"test"+getBasePath()
    
    '''
    Read All tweets and create two different set for Mood and Activity
    '''
    
    classActList,docActList = readallTweets(trainDPath)
    
    #print docActList
    '''
    Create FeatureList for Activity in SVM format
    '''
    tfActFeatureList = dumpTfFeatureList(docActList,True,stopWordList)
    print "Training Activity Tweet Length",len(tfActFeatureList)
    print "Training Class List ",len(classActList)

    #print termSet
   
    return tfActFeatureList,classActList

def writePickle(tfFeatureList,classMoodList,classActList):
    pickle.dump(tfFeatureList, open("SVM_train_ACT_X_Feature_TF"+".txt","wb"))
    pickle.dump(classActList, open("SVM_train_ACT_Y_ClassList"+".txt","wb"))

    return

def main():
    print "**** Basic SVM  Training Data Set Generation Module******" 
    #classType = "entertainment,business,politics"
    tfFeatureList,classActList = init_ActTrain() 
    #writePickle(tfFeatureList,classActList)
    #print tfFeatureList
    print "~~~~~~Training Data Set Collection Done~~~~~~~~"
    #testCMoodList,testCActList,doctestList = readallTweets(testDPath)
    #tfFeatureTestList = dumpTfFeatureList(doctestList,False,stopWordList)
    print "Test Data Set Feature Extraction Done"
    #pickle.dump(tfFeatureTestList, open("SVM_test_MOOD_X_Feature_TF"+".txt","wb"))
    #pickle.dump(testCMoodList, open("SVM_test_MOOD_X_LABELED_CLASS_TF"+".txt","wb"))
    #pickle.dump(testCActList, open("SVM_test_ACT_X_LABELED_CLASS_TF"+".txt","wb"))
    print "Dumping Done"
   
    return

if __name__ == '__main__':
    main()
