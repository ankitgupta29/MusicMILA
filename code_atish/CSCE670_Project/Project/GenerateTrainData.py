'''
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
class MoodList:
    ML_HAPPY = 0;
    ML_CALM = 1;
    ML_ANGRY = 2;
    ML_SAD = 3;
    ML_LOVE = 4;
        
# 0 does not belong to any class        
class ACTList:
    ACT_DAILY = 1;
    ACT_CHILLING = 2;
    ACT_PHYSICAL = 3;
    ACT_RELAX = 4;
    ACT_MENTAL = 5;

def getBasePath():
    if os.name == 'nt': # Windows
        basePath = '\\\\'
    else:
        basePath = '/'
    print basePath
    return basePath
   
    
    
def createTFdict(doc,bTrain,stopWordList):
    tfdict = defaultdict()
    #termList = [p for p in doc.lower().split() for p in re.findall(r"[\w]+",p)]
    tList = doc.lower().split()
    for tIndex,term in enumerate(tList):
        #print term
        if "@" in term or (len(term) <2) or (term in stopWordList):
            del tList[tIndex]
    termList = [p for p in tList  for p in re.findall(r"[0-9A-Za-z'\&\-\.\/()=:;,_^ ->\]\[]+",p)]
    #print termList
    for fterm in termList:
        if fterm in tfdict :
            tfdict[fterm] = tfdict[fterm]+1
        else:
            tfdict[fterm] = 1
        if(bTrain):
            termSet.add(fterm)         

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
    actDirPath = os.getcwd()+getBasePath()+"activity"+getBasePath()
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

def mapMood2Class(moodType):
    moodClassNum = -1
    if moodType == "happy":
        moodClassNum = MoodList.ML_HAPPY
    elif moodType == "calm":
        moodClassNum = MoodList.ML_CALM
    elif moodType == "angry":
        moodClassNum = MoodList.ML_ANGRY
    elif moodType == "sad":
        moodClassNum = MoodList.ML_SAD
    elif moodType == "love":
        moodClassNum = MoodList.ML_LOVE
    return moodClassNum     

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
    classMoodList = []
    docList = []
    classActList = []
    for file in filList:
        print file
        reader = csv.reader(open(path+file,'r'))
        totalRowLen = 0;
        for rIndex,row in enumerate(reader):
            #print row[TDProp.TD_TEXT] //Text
            totalRowLen = totalRowLen+1
            print rIndex,len(row)
            if(rIndex > 0):
                #print rIndex,row[TDProp.TD_ACT1] #//Mood1
                moodType = row[TDProp.TD_MOOD1]
                classMoodList.append(mapMood2Class(moodType))
                docList.append( row[TDProp.TD_TEXT])
                if(len(row)==TDProp.TD_ACT1+1):
                    print "Row Len",len(row)
                    print rIndex,row[TDProp.TD_ACT1]
                    classActList.append(mapActivity2Class(row[TDProp.TD_ACT1]))
                else:
                    classActList.append(0)
        print classActList
        print "NumRows",totalRowLen
        
    return classMoodList,classActList,docList

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
def main():
    print "**** Basic SVM  Training Data Set Generation Module******" 
    #classType = "entertainment,business,politics"
    stopWordList = createStopWList()
    addSmileyFeatures()
    addActivityFeatures()
    print "~~~~~~Begin Creating the dataset~~~~~~~~"
    trainDPath = os.getcwd()+getBasePath()+"train"+getBasePath()
    testDPath = os.getcwd()+getBasePath()+"test"+getBasePath()
    classMoodList,classActList,docList = readallTweets(trainDPath)
    
    #print docList
    tfFeatureList = dumpTfFeatureList(docList,True,stopWordList)
    #pickle.dump(tfFeatureList, open("SVM_train_MOOD_X_Feature_TF"+".txt","wb"))
    #pickle.dump(classMoodList, open("SVM_train_MOOD_Y_ClassList"+".txt","wb"))     
    #pickle.dump(classActList, open("SVM_train_ACT_Y_ClassList"+".txt","wb"))
    #print tfFeatureList
    print "~~~~~~Training Data Set Collection Done~~~~~~~~"
    testCMoodList,testCActList,doctestList = readallTweets(testDPath)
    tfFeatureTestList = dumpTfFeatureList(doctestList,False,stopWordList)
    print "Test Data Set Feature Extraction Done"
    pickle.dump(tfFeatureTestList, open("SVM_test_MOOD_X_Feature_TF"+".txt","wb"))
    pickle.dump(testCMoodList, open("SVM_test_MOOD_X_LABELED_CLASS_TF"+".txt","wb"))
    pickle.dump(testCActList, open("SVM_test_ACT_X_LABELED_CLASS_TF"+".txt","wb"))
    print "Dumping Done"
    
    
    '''
    for cIndex,cType in enumerate(classType.split(",")):
        resultList = pickle.load(open("DocumentList_train_"+cType+".txt","rb"))
        for dIndex,doc in enumerate(resultList):
            tfDict = createTFdict(doc,True)
            #print tfDict
            tfDictList.append(tfDict)
            tfDocList.append(cIndex)
        #print termSet, len(tfDictList)    
        totalNumDocs = totalNumDocs+len(resultList)
        
            #print tfDictList 
        print "All Documents from Class [%s] is Done TOtal Terms [%s]" %(cType,len(termSet))
        #print tfFeatureList
    print "Total Documents in Corpus [%s]" %(len(termSet))
    print tfDocList
    pickle.dump(tfDocList, open("SVM_train_Y_ClassList"+".txt","wb"))       
    tfFeatureList = getFeatureVector(totalNumDocs,tfFeatureList,tfDictList)      
    pickle.dump(tfFeatureList, open("SVM_train_X_Feature_TF"+".txt","wb"))
    
    print "~~~~~~Training Data Set Collection Done~~~~~~~~"
    #for cIndex,cType in enumerate(classType.split(",")):
    for cIndex,cType in enumerate(classType.split(",")):
        totalNumDocs= 0
        tfFeatureList = []
        tfDictList = []
        print tfFeatureList
    
        resultList = pickle.load(open("DocumentList_test_"+cType+".txt","rb"))
        for dIndex,doc in enumerate(resultList):
            tfDict = createTFdict(doc,False)
            #print tfDict
            tfDictList.append(tfDict)
        #print termSet, len(tfDictList)    
        totalNumDocs = totalNumDocs+len(resultList)
        
            #print tfDictList 
        print "All Documents from Test Class [%s] is Done TOtal Terms [%s]" %(cType,len(termSet))
            #print tfFeatureList
        print "Total terms in Test Corpus [%s]" %(len(termSet))
        print tfFeatureList    
        tfFeatureList = getFeatureVector(totalNumDocs,tfFeatureList,tfDictList)   
        pickle.dump(tfFeatureList, open("SVM_test_X_Feature_TF"+str(cIndex)+".txt","wb"))
        print "Dumping Done"
    '''
    return

if __name__ == '__main__':
    main()