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
actTermSet = set()
classList = []

def log2( x ):
    return math.log( x ) / math.log( 2 )
#Feature Selection Code
class NewsClass:
    def __init__(self):
            self.className = ""
            self.numDocs = 0
            self.docList = []
            self.tfDict = defaultdict(list) #this dictionary represents term : tf score 
            self.numTerms = 0
            self.tCondProb = defaultdict()
            self.priorProb = 0
            self.termDocList = defaultdict()
            self.termMIDictL = defaultdict()
    def addDocToClass(self,doc):
        self.numDocs = self.numDocs+1
        termList = [p for p in doc.lower().split() for p in re.findall(r"[\w]+",p)]
        bfirstTime = True
        for term in termList:
            if term in self.termDocList and bfirstTime:
                self.termDocList[term] = self.termDocList[term]+1
                bfirstTime = False
            else:
                self.termDocList[term] = 1
                bfirstTime = False
                termSet.add(term) 
            if term in self.tfDict:
                count = self.tfDict.get(term)
                count = count + 1
                self.tfDict[term] = count
                self.numTerms = self.numTerms+1
            else:
                self.tfDict[term] = 1
                self.numTerms = self.numTerms+1
                
def findTotalDocForthisTerm(term,classList):
    numDocs = 0
    for eachClass in classList:
        if term in eachClass.termDocList:
            numDocs = numDocs+eachClass.termDocList[term]
    #print "total Docs with the term [%s] = [%d]" %(term,numDocs) 
    return numDocs
def selectFeature(totalNDocs):
    for eachClass in classList:
        #print "For Class",eachClass.className
        for eachTerm in eachClass.tfDict:
            fact1= 0.0
            fact2 = 0.0
            fact3 = 0.0
            fact4 = 0.0
            print "Term %s present in %d docs" %(eachTerm,eachClass.termDocList[eachTerm])
            print "Total terms in the class ",len(eachClass.tfDict)
            N11 = eachClass.termDocList[eachTerm]
            print N11,eachClass.numDocs
            N01 = eachClass.numDocs - N11
            N10 = findTotalDocForthisTerm(eachTerm,classList)-N11
            N00 = totalNDocs-N10-eachClass.numDocs
            
            if (N11 == 0.0):
                N11 = 1
            if (N01==0.0):
                N01=1.0
            if(N10 == 0.0):
                N10 =1.0
            if(N00==0.0):
                N00 = 1.0
            print N00,N01,N11,N10
            fact1 = (N11/totalNDocs) * log2((totalNDocs*N11)/((N11+N10)*(N11+N01)))
            fact2 = (N01/totalNDocs) * log2((totalNDocs*N01)/((N01+N00)*(N11+N01)))
            fact3 = (N10/totalNDocs) * log2((totalNDocs*N10)/((N11+N10)*(N10+N00)))
            fact4 = (N00/totalNDocs) * log2((totalNDocs*N00)/((N01+N00)*(N10+N00)))
            '''
            if (N11 > 0.0):
                fact1 = (N11/totalNumDocs) * log2((totalNumDocs*N11)/((N11+N10)*(N11+N01)))
            if (N01>0.0):
                fact2 = (N01/totalNumDocs) * log2((totalNumDocs*N01)/((N01+N00)*(N11+N01)))
            if(N10 > 0.0):
                fact3 = (N10/totalNumDocs) * log2((totalNumDocs*N10)/((N11+N10)*(N10+N00)))
            if(N00 > 0.0):
                fact4 = (N00/totalNumDocs) * log2((totalNumDocs*N00)/((N01+N00)*(N10+N00)))
            '''
            valMI = fact1+fact2+fact3+fact4
            print "########MI Value is ##########",valMI
            eachClass.termMIDictL[eachTerm] = valMI
        print eachClass.termMIDictL
        
        totalTerm  = len(eachClass.termMIDictL)
        #print totalTerm
        tempDict = sorted(eachClass.termMIDictL.items(), key=lambda x: x[1],reverse = True)
        #print tempDict
        leastMICount = 0
        bestFeatureNUm = 6000 # change this number to find out best F1 Value
        for index,eachKey in enumerate(tempDict):     
            #print eachClass.termMIDictL[eachKey[0]]
            #del eachClass.termMIDictL[eachKey[0]]
            #leastMICount = leastMICount+1
            #if((totalTerm-leastMICount) <= bestFeatureNUm):
            #break
            if(index > bestFeatureNUm):
                if eachClass.tCondProb.has_key(eachKey[0]):
                    del eachClass.tCondProb[eachKey[0]]
        #print len(eachClass.termMIDictL)
        #print eachClass.termMIDictL
    return 


#Feature Selection Code
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


    
def addLDAFeatures():
    ldaDirPath = os.getcwd()+getBasePath()+"lda"+getBasePath()
    print ldaDirPath
    topicList = open(ldaDirPath+"ldaTopics2.txt",'r').readlines()
    return topicList
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

def mapClass2Mood(moodClassNum):
    moodClass = ""
    if moodClassNum == MoodList.ML_HAPPY:
        moodClass = "happy"
    elif moodClassNum == MoodList.ML_CALM:
        moodClass = "calm"
    elif moodClassNum == MoodList.ML_ANGRY:
        moodClass = "Angry"
    elif moodClassNum == MoodList.ML_SAD:
        moodClass = "sad"
    elif moodClassNum == MoodList.ML_LOVE:
        moodClass = "love"
    
    return moodClass    

def updateFeatureDict(cType,doc):
    classObj = NewsClass()
    classObj.className = cType
    classObj.addDocToClass(doc)
    classList.append(classObj)
    
def readallTweets(path):
    filList =  os.listdir(path)
    classMoodList = []
    docList = []
    ldaFile = open("lda_mmila_input.txt",'wb')
    for f1 in filList:
        print "************ File Found*****************",f1
        reader = csv.reader(open(path+f1,'r'))
        totalRowLen = 0;
        for rIndex,row in enumerate(reader):
            #print row[TDProp.TD_TEXT] //Text
            totalRowLen = totalRowLen+1
            print rIndex,len(row)
            if(rIndex > 0):
                #print rIndex,row[TDProp.TD_ACT1] #//Mood1
                text = row[TDProp.TD_TEXT]
                ldaFile.write(str(rIndex)+"\t"+'X'+"\t"+text+"\n") 
                moodType = row[TDProp.TD_MOOD1]
                updateFeatureDict(moodType,text)
                classMoodList.append(mapMood2Class(moodType))
                docList.append( row[TDProp.TD_TEXT])
    return classMoodList,docList

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
    #add LDA feature
    topicList = addLDAFeatures()
    for docIndex,doc in enumerate(tfFeatureList):
        print topicList[docIndex].split()
        tfFeatureList[docIndex].extend(topicList[docIndex].split())

        #addLDAFeatures(tfFeatureList,docIndex)
                         
    return tfFeatureList

def createTestMoodFVec(text):
    dummyList = []
    dummyList.append(text)
    #tfFeatureList,classMoodList,classActList = init() 
    stopWordList = createStopWList()
    featureTList = dumpTfFeatureList(dummyList,False,stopWordList)
    return featureTList

def init_MoodTrain():
    
    stopWordList = createStopWList()
    addSmileyFeatures()
    print "~~~~~~Begin Creating the dataset~~~~~~~~"
    trainDPath = os.getcwd()+getBasePath()+"train"+getBasePath()
    testDPath = os.getcwd()+getBasePath()+"test"+getBasePath()
    
    '''
    Read All tweets and create two different set for Mood and Activity
    '''
    
    classMoodList,docList = readallTweets(trainDPath)
    selectFeature(len(docList))
    '''
    Create FeatureList for Mood in SVM format
    '''
    tfMoodFeatureList = dumpTfFeatureList(docList,True,stopWordList)
    #print termSet
    #print docList
 
    return tfMoodFeatureList,classMoodList

def writePickle(tfFeatureList,classMoodList):
    pickle.dump(tfFeatureList, open("SVM_train_MOOD_X_Feature_TF"+".txt","wb"))
    pickle.dump(classMoodList, open("SVM_train_MOOD_Y_ClassList"+".txt","wb"))     

    return

def main():
    print "**** Basic SVM  Training Data Set Generation Module******" 
    classType = "entertainment,business,politics"
    stop1WordList = createStopWList()
    tfFeatureList,classMoodList = init_MoodTrain() 
    writePickle(tfFeatureList,classMoodList)
    #print tfFeatureList
    print "########~~~~~~Training Data Set Collection Done~~~~~~~~"
    
    testDPath = os.getcwd()+getBasePath()+"test"+getBasePath()
    print "######Test Data Path",testDPath
    testCMoodList,doctestList = readallTweets(testDPath)
    tfFeatureTestList = dumpTfFeatureList(doctestList,False,stop1WordList)
    print "Test Data Set Feature Extraction Done"
    pickle.dump(tfFeatureTestList, open("SVM_test_MOOD_X_Feature_TF"+".txt","wb"))
    pickle.dump(testCMoodList, open("SVM_test_MOOD_Y_ClassList"+".txt","wb"))
    #pickle.dump(testCActList, open("SVM_test_ACT_X_LABELED_CLASS_TF"+".txt","wb"))
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
