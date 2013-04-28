import os,re,json
from collections import defaultdict

artistLocationDict = defaultdict()
songPropertyDict = defaultdict()

'''
#this will fetch artist and its location from artist_location.txt
f = file('artist_location.txt','rb')
for line in f:
	line  = line.split('<SEP>')
	artist = line[-2].lower()
	location = line[-1][0:-1].lower()
	artistLocationDict.setdefault(location,[]).append(artist)
'''

'''
#this will fetch track,gener,artist and title from mst_genre_dataset.txt

f = open('msd_genre_dataset.txt','rb')
for line in f.readlines():
	line     = line.split(',')
	track_id = line[1]
	genre    = line[0]
	artist   = line[2]
	title    = line[3]	
	print track_id,genre,artist,title
	
'''

#this fill fetch hotness from song and return track_id and its hotness
#python display_song.py  -summary msd_summary_file.h5 100000



'''
json.dump(artistLocationDict,open('ArtistLocationOnly.txt','wb'))


for key in  artistLocationDict.keys():
	if 'california' in key:
		print key
'''


