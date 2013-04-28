import os,re,json
from collections import defaultdict

artistLocationDict = defaultdict()

f = file('artist_location.txt','rb')
for line in f:
	line  = line.split('<SEP>')
	artist = line[-2].lower()
	location = line[-1][0:-1].lower()
	artistLocationDict.setdefault(location,[]).append(artist)

'''
json.dump(artistLocationDict,open('ArtistLocationOnly.txt','wb'))


for key in  artistLocationDict.keys():
	if 'california' in key:
		print key
'''


