import sys,os,re

cd = os.getcwd()
new = cd + '\\wordlists\\'
os.chdir(new)

listing  = os.listdir(new)

happy = []
angry = []
love = []

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

	if file == 'love.txt':
		f = open(file,'rb')
                for line in f.readlines():
                        line  = line[11:]
                        wordList = re.sub("[^\w]", " ",  line).split()
                        for word in wordList:
                                love.append(word)
os.chdir(cd)
