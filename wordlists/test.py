import re

f = open('calm.txt','rb')

for line in f.readlines():
	wordlist = line.split(',')
fw = open('calm2.txt','ab')
for word in wordlist:
	fw.write(word)
	fw.write('\n')
