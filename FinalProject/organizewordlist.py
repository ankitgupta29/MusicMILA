import os,re

cd = os.getcwd()
new = cd + '/wordlists/UnorganizedFiles/'
new2 = cd + '/wordlists/'
stoplist = []
f = open('stopword.txt','rb')
for word in f.readlines():
	stoplist.append(word[0:-1])

os.chdir(new)
for file in os.listdir(new):
	os.chdir(new)
	f = open(file,'rb')
	#outfile = file + '_'+''
	os.chdir(new2)
	fw = open(file,'ab')
	for line in f.readlines():
		wordlist = re.sub("[^\w]", " ",  line).split()
		for word in wordlist:
			if word not in stoplist and len(word) > 2:			
				result = ''.join([i for i in word if not i.isdigit()])
				fw.write(result)
				fw.write('\n')
				
				

