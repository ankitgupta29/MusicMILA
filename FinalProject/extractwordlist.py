import sys,os,re
from FileUtil import getAllFileinDir
cd = os.getcwd()
new = cd + '/wordlists/'
os.chdir(new)

#listing  = os.listdir(new)
listing = getAllFileinDir(new)
#print listing

happy = []
angry = []
love = []
physical = []
mental = []
daily = []
relaxing = []
chilling = []
sad = []
calm = []


for filePath in listing:
	fileName = os.path.basename(filePath)
	print "######",fileName
	if fileName == 'joy.txt' or 'surprise.txt':
		f = open(filePath,'rb')
		for line in f.readlines():
			line  = line[11:]
			wordList = re.sub("[^\w]", " ",  line).split()
		      	for word in wordList:
				happy.append(word)

	if fileName == 'disgust.txt' or 'anger.txt':
		f = open(filePath,'rb')
                for line in f.readlines():
                        line  = line[11:]
                        wordList = re.sub("[^\w]", " ",  line).split()
                        for word in wordList:
				angry.append(word)
				
	if fileName == 'sad.txt':
		f = open(filePath,'rb')
                for line in f.readlines():
                        line  = line[11:]
                        wordList = re.sub("[^\w]", " ",  line).split()
                        for word in wordList:
				sad.append(word)
        if fileName == 'calm.txt':
                f = open(filePath,'rb')
                for line in f.readlines():

                        wordList = re.sub("[^\w]", " ",  line).split()
                        for word in wordList:
                                calm.append(word)
				
	if fileName == 'love.txt':
		f = open(filePath,'rb')
                for line in f.readlines():
                      
                        wordList = re.sub("[^\w]", " ",  line).split()
                        for word in wordList:
                                love.append(word)
                                
	if fileName == 'physical.txt':
		f = open(filePath,'rb')
                for line in f.readlines():
                   
                        wordList = re.sub("[^\w]", " ",  line).split()
                        for word in wordList:
                                physical.append(word)
                                
	if fileName == 'mental.txt':
		f = open(filePath,'rb')
                for line in f.readlines():
                      
                        wordList = re.sub("[^\w]", " ",  line).split()
                        for word in wordList:
				mental.append(word)

	if fileName == 'daily.txt':
		f = open(filePath,'rb')
                for line in f.readlines():
                   
                        wordList = re.sub("[^\w]", " ",  line).split()
                        for word in wordList:
                                daily.append(word)
                                
	if fileName == 'chilling.txt':
		f = open(filePath,'rb')
                for line in f.readlines():
                     
                        wordList = re.sub("[^\w]", " ",  line).split()
                        for word in wordList:
                                chilling.append(word)
                                
	if fileName == 'relaxing.txt':
		f = open(filePath,'rb')
                for line in f.readlines():
                       
                        wordList = re.sub("[^\w]", " ",  line).split()
                        for word in wordList:
                                relaxing.append(word)
                            
os.chdir(cd)
