import re,os,operator,json
import extractwordlist
from collections import defaultdict

songTrackIdMoodDict     = defaultdict()
songTrackIdActivityDict = defaultdict()

happy	 = extractwordlist.happy
sad      = extractwordlist.sad 
calm     = extractwordlist.calm
angry    = extractwordlist.angry
love     = extractwordlist.love
physical = extractwordlist.physical
mental   = extractwordlist.mental
daily    = extractwordlist.daily
chilling = extractwordlist.chilling
relaxing = extractwordlist.relaxing


stopword = []
fs = open('stopword.txt','rb')
for line in fs.readlines():
	stopword.append(line[:-1])

cd = os.getcwd()
new = cd + '/SongClassifyList/'

listofmood =     ['happy','sad','calm','angry','love']		
listofactivity = ['physical','mental','daily','chilling','relaxing']

def main():
	global songTrackIdMoodDict,songTrackIdActivityDict
	f = open('mxm_dataset_train.txt','rb')
	#f = open('tempsong.txt','rb')
        string = f.readline()
        globalwordlist = string.split(',')
	#print globalwordlist
	i = 0
	for line in f.readlines():
		#i = i +1
		#if i == 1000:
		#	break
		moodlist      = [0,0,0,0,0]
		activitylist  = [0,0,0,0,0]
		songworddict  = defaultdict(int)
		track_id = (line.split(','))[0]
		#if track_id == 'TRFCOOU128F427AEC0'or 'TRABWFM128F424D86A':
		#	print "match"
		#	raw_input()
		songindexlist = (line.split(','))[2:]		
		for item in songindexlist:
			index = int((item.split(':'))[0])
			#value = int(item.split(':')[1])
			if index < 4729:
				songworddict[globalwordlist[int((item.split(':'))[0])]] = int(item.split(':')[1])
		
		for word in songworddict:
			if word not in stopword:
				if word in happy:	
					moodlist[0] = moodlist[0] + int(songworddict[word])
		
                                if word in sad:
                                        moodlist[1] = moodlist[1] + int(songworddict[word])
                        
                                if word in calm:
                                        moodlist[2] = moodlist[2] + int(songworddict[word])
                        
                                if word in angry:
                                        moodlist[3] = moodlist[3] + int(songworddict[word])
                        	
                                if word in love:
                                        moodlist[4] = moodlist[4] + int(songworddict[word])
                        	
                                if word in physical:
                                        activitylist[0] = activitylist[0] + int(songworddict[word])
                        
                                if word in mental:
                          	        activitylist[1] = activitylist[1] + int(songworddict[word])
                        
                                if word in daily:
                                        activitylist[2] = activitylist[2] + int(songworddict[word])

                                if word in chilling:
                                        activitylist[3] = activitylist[3] + int(songworddict[word])

                                if word in relaxing:
                                        activitylist[4] = activitylist[4] + int(songworddict[word])
				
		index1, value1 = max(enumerate(moodlist), key=operator.itemgetter(1))				       
		index2, value2 = max(enumerate(activitylist), key=operator.itemgetter(1))
		songTrackIdMoodDict.setdefault(listofmood[index1],[]).append(track_id)
		songTrackIdActivityDict.setdefault(listofactivity[index2],[]).append(track_id)
			
	os.chdir(new)
	json.dump(songTrackIdMoodDict,open('songIDMoodDict.json','wb'))
	json.dump(songTrackIdActivityDict,open('songIDActivityDict.json','wb'))	
		
	os.chdir(cd)

if __name__ == '__main__':
 main()

