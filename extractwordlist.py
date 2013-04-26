import sys,os,re

cd = os.getcwd()
new = cd + '/wordlists/'
os.chdir(new)

listing  = os.listdir(new)

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

for file in listing:
	if file == 'joy.txt' or 'surprise.txt':
		f = open(file,'rb')
		for line in f.readlines():
			line  = line[11:]
			wordList = re.sub("[^\w]", " ",  line).split()
		      	for word in wordList:
				happy.append(word)

	if file == 'disgust.txt' or 'anger.txt':
		f = open(file,'rb')
                for line in f.readlines():
                        line  = line[11:]
                        wordList = re.sub("[^\w]", " ",  line).split()
                        for word in wordList:
				angry.append(word)
				
	if file == 'sad.txt':
		f = open(file,'rb')
                for line in f.readlines():
                        line  = line[11:]
                        wordList = re.sub("[^\w]", " ",  line).split()
                        for word in wordList:
				sad.append(word)
        if file == 'calm.txt':
                f = open(file,'rb')
                for line in f.readlines():

                        wordList = re.sub("[^\w]", " ",  line).split()
                        for word in wordList:
                                calm.append(word)
				
	if file == 'love.txt':
		f = open(file,'rb')
                for line in f.readlines():
                      
                        wordList = re.sub("[^\w]", " ",  line).split()
                        for word in wordList:
                                love.append(word)
                                
	if file == 'physical.txt':
		f = open(file,'rb')
                for line in f.readlines():
                   
                        wordList = re.sub("[^\w]", " ",  line).split()
                        for word in wordList:
                                physical.append(word)
                                
	if file == 'mental.txt':
		f = open(file,'rb')
                for line in f.readlines():
                      
                        wordList = re.sub("[^\w]", " ",  line).split()
                        for word in wordList:
				mental.append(word)

	if file == 'daily.txt':
		f = open(file,'rb')
                for line in f.readlines():
                   
                        wordList = re.sub("[^\w]", " ",  line).split()
                        for word in wordList:
                                daily.append(word)
                                
	if file == 'chilling.txt':
		f = open(file,'rb')
                for line in f.readlines():
                     
                        wordList = re.sub("[^\w]", " ",  line).split()
                        for word in wordList:
                                chilling.append(word)
                                
	if file == 'relaxing.txt':
		f = open(file,'rb')
                for line in f.readlines():
                       
                        wordList = re.sub("[^\w]", " ",  line).split()
                        for word in wordList:
                                relaxing.append(word)
                            
os.chdir(cd)
