import os,re,sys,json
import simplejson
from collections import defaultdict
cd = os.getcwd()
new = cd + '/SongClassifyList/'



activitygenre = {'physical': ['metal','punk','dance and electronica'],'mental':['classic pop and rock'],'daily':['classic pop and rock','Soul and Reggae'],'chilling':['metal','punk','soul and Reggae'],'relaxing': ['classic pop and rock'] }

moodgenre = {'angry': ['metal'],'happy':['Soul and Reggae','folk','classic pop and rock'],'sad' :['classic pop and rock'],'calm' : ['folk','classic pop and rock'] }


os.chdir(new)
print os.getcwd()
fa =  open('songIDActivityDict.json','r')
fm =  open('songIDMoodDict.json','r')
fs = open('songProperty.json','r')

moodlist = []
activitylist = []

trackIdActivityDict = defaultdict()
trackIdMoodDict = defaultdict()
songPropertyDict = defaultdict()
trackDigitalIdDict = defaultdict()
activitygenredict = defaultdict(int)
moodgenredict = defaultdict(int)
moodsortedlist = []
activitysortedlist = []



for line in fa.readlines():
	trackIdActivityDict = simplejson.loads(unicode(line),encoding="UTF-8")
	#print trackIdActivityDict


for line in fm.readlines():
        trackIdMoodDict = simplejson.loads(unicode(line),encoding="UTF-8")


for line in fs.readlines():
        songPropertyDict = simplejson.loads(unicode(line),encoding="UTF-8")

'''
for key in songPropertyDict:
	print key,songPropertyDict[key]
'''

def getActivityGenre(activity):
	sortedlist = []
	if not trackIdActivityDict.has_key(activity):
		print "Empty Acitvity List"
		return sortedlist
	activitylist = trackIdActivityDict[activity]
	for track in activitylist:
		if songPropertyDict.has_key(track):
			trackProp = songPropertyDict[track]
			#print trackProp	
			value = trackProp[0][0]
			
			#print "Songe Genre is    : ",value
			#print "Activity Genre is : ",activitygenre[activity]
			#print value,activitygenre[activity]
			
			for item in activitygenre[activity]:
				if item == value:
					#print "Song added"	
					activitygenredict.setdefault(track,[]).append(trackProp)
					sortedlist.append(track)
			#print "==============================================="
	return sortedlist
		
		
def getMoodGenre(mood):
	print trackIdMoodDict.keys()
        sortedlist = []
	if not trackIdMoodDict.has_key(mood):
		print 'Empty Mood List'
		return sortedlist
	moodlist = trackIdMoodDict[mood]
        for track in moodlist:
                if songPropertyDict.has_key(track):
                        trackProp = songPropertyDict[track]
                        #print trackProp        
                        value = trackProp[0][0]

                        #print "Songe Genre is    : ",value
                        #print "Activity Genre is : ",activitygenre[activity]
                        #print value,activitygenre[activity]

                        for item in moodgenre[mood]:
                                if item == value:
                                        #print "Song added"     
                                        moodgenredict.setdefault(track,[]).append(trackProp)
                                        sortedlist.append(track)
                        #print "==============================================="
        return sortedlist		

	
os.chdir(cd)
def fetchSong(mood_input,activity_input,location_input):
	
	trackScoreDict = defaultdict(float)		
	print mood_input,activity_input,location_input
	locationlist = (location_input.lower()).split()
	templist =[]
	activitysortedlist = getActivityGenre(activity_input.lower())
	#print activitysortedlist
	templist.append(activitysortedlist)
	
	moodsortedlist = getMoodGenre(mood_input.lower())
        #print moodsortedlist
	#print len(activitysortedlist)
	#print len(moodsortedlist)
	templist.append(moodsortedlist)
	
	result = reduce(set.union,map(set,templist))


	for track in result:
		#print track
		if track in moodsortedlist:
			trackScoreDict[track] = trackScoreDict[track] + 0.5
		#print trackScoreDict[track]
		if track in activitysortedlist:
                        trackScoreDict[track] = trackScoreDict[track] + 0.2
		#print trackScoreDict[track]
		trackLocation = songPropertyDict[track][0][3]
		trackLocation = str(trackLocation[0]).split(',')
		isfound = False
		for x in location_input:
			for y in trackLocation:
				if x in y:
					trackScoreDict[track] = trackScoreDict[track] + 0.3
					isfound = True
					break
			if isfound:
				break
		#print trackScoreDict[track]
		hottness =songPropertyDict[track][1]
		#print hottness
		trackScoreDict[track] = trackScoreDict[track] * hottness
		digital_id = songPropertyDict[track][2]
		artist = songPropertyDict[track][0][2]
		title = songPropertyDict[track][0][1]
		tup = (digital_id,artist,title)
		trackDigitalIdDict[track] = tup
		#print trackScoreDict[track]
		#print "======================================\n"
	
	#for key in trackScoreDict:
		#print key,trackScoreDict[key]
	return trackScoreDict,trackDigitalIdDict
def main():

	mood_input = 'happy'
	activity_input = 'physical'
	location_input = 'ohio'
	fetchSong(mood_input,activity_input,location_input)
	
			

if __name__ == '__main__':
 main()






