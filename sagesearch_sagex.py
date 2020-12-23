import glob
import re
import os
import subprocess
import sys
import os.path
from os import path

import imdb
ia = imdb.IMDb()

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from tvmaze.api import Api

import requests
import json

# showYear = rawJson['MediaFile']['Airing']['Show']['ShowYear']
# season = rawJson['MediaFile']['MediaFileMetadataProperties']['SeasonNumber']
# episode = rawJson['MediaFile']['MediaFileMetadataProperties']['EpisodeNumber']

# isMovie = rawJson['MediaFile']['Airing']['Show']['IsMovie']
# imdbid = rawJson['MediaFile']['MediaFileMetadataProperties']['IMDBID']

# print(isMovie)


def fun(episodeList,token):  
    
	bestRatio = 0;
	bestRatioIndex = 0;
	for index, item in enumerate(episodeList):
	
		epname = item.name
	
		ratio = fuzz.partial_ratio(token,epname)
		if ratio > bestRatio:
			bestRatio = ratio
			season = item.season
			episode = item.number
			bName = epname;
			
	d = dict();
	d['season'] = season
	d['episode'] = episode
	d['title'] = bName
	return d  
	

api = Api()


linkDirectory = 'E:\\XBMCLinks\\New TV\\'
movieLinkDirectory = 'E:\\XBMCLinks\\New Movies\\'

dbDirectory = 'E:\\XBMCLinks\\dB\\'

yearlist = ['E:\\SageTVShowsNew\*.ts','F:\\SageTVShowsNew\*.ts']

for year in yearlist:
	for name in glob.glob(year): 
		
		found = 0
		#season = re.findall(r"(?:s|season)(\d{2})(?:e|x|episode|\n)(\d{2})", name, re.I)
		#episode = re.findall(r"(?:e|x|episode|\n)(\d{2})", name, re.I)
		result = re.search('New\\\(.*)', name)
		justFileName = result.group(1)
		
		dbFile = dbDirectory + justFileName + '.found';
		if path.exists(dbFile):
			#print('skipping: ')
			continue;
		
		result2 = re.search('(.*)-', justFileName)
		show = result2.group(1)
		indexOfFirstDash = justFileName.find('-')
		
		#showName = re.sub(r"(\w)([A-Z])", r"\1 \2", justFileName[0:indexOfFirstDash])
		#showName = re.sub(r"(\w)([A-Z])", r"\1 \2", justFileName[0:indexOfFirstDash])
		#showName = re.sub(r"(\w)(and)", r"\1 \2", showName)

		r = requests.get('http://192.168.1.4:8080/sagex/api?c=GetMediaFileForFilePath&1=' + name + '&encoder=json')
		rawJson = r.json()
		showName = rawJson['MediaFile']['MediaTitle']
		showName = showName.replace(':', '')
		
		imdbid = 0;
		if rawJson['MediaFile']['MediaFileMetadataProperties']:
			if 'IMDBID' in rawJson['MediaFile']['MediaFileMetadataProperties']:
				imdbid = rawJson['MediaFile']['MediaFileMetadataProperties']['IMDBID']
				
		
		result = re.search(r"(?:s|season)(\d{2})(?:e|x|episode|\n)(\d{2})", name, re.I)
		
		if result == None:
			restOfFileName = justFileName[indexOfFirstDash+1:len(justFileName)-3]
			
			if len(restOfFileName) <= 10:
				# print(showName)
				if imdbid==0:
					movies = ia.search_movie(showName)
					if not movies:
						continue
					curMovie = movies[0]
				else:
					shortID = imdbid[2:len(imdbid)]
					
					if not shortID:
						continue
					curMovie = ia.get_movie(shortID)
									
				
				if curMovie['kind'] == 'movie' or curMovie['kind'] == 'tv movie':
					year = str(curMovie['year'])
					title = str(curMovie['title'])
					title = title.replace(':', '')
					
					movieLink = movieLinkDirectory + title + ' (' + year + ')\\' + title + ' (' + year + ').ts'
					
					subprocess.call(['cmd', '/c', 'mkdir', movieLinkDirectory + title + ' (' + year + ')'])
					subprocess.call(['cmd', '/c', 'mklink', movieLink, name])
					found = 1;
				else:
					movieLink = movieLinkDirectory + showName + '\\' + showName + '.ts'
					#print(movieLink)
					subprocess.call(['cmd', '/c', 'mkdir', movieLinkDirectory + showName])
					subprocess.call(['cmd', '/c', 'mklink', movieLink, name])
					found = 1;
			else:
				
				indexOfNextDash = restOfFileName.find('-')
				episodeTitle = re.sub(r"(\w)([A-Z])", r"\1 \2", restOfFileName[0:indexOfNextDash])
				
				# print(showName)
				show2 = api.search.shows(showName)
				if len(show2) == 0:
					continue
				show = show2[0]
				
					
				# print(show)
				episodeList = api.show.episodes(show.id)
				res = fun(episodeList,episodeTitle)
				season = str(res['season'])
				episode = str(res['episode'])
				linkName = linkDirectory + showName + '\\Season ' + season + '\\' + showName + ' S' + season + 'E' + episode + '.ts'
				#print(linkName)
				subprocess.call(['cmd', '/c', 'mkdir', linkDirectory + showName])
				subprocess.call(['cmd', '/c', 'mkdir', linkDirectory + showName + '\\Season ' + season + '\\'])
				subprocess.call(['cmd', '/c', 'mklink', linkName, name])
				found = 1
		else:	
			# print(result)	
			season = result.group(1)
			episode = result.group(2)
			if episode:
				linkName = linkDirectory + showName + '\\Season ' + season + '\\' + showName + ' S' + season + 'E' + episode + '.ts'
				#print(linkName)
				subprocess.call(['cmd', '/c', 'mkdir', linkDirectory + showName])
				subprocess.call(['cmd', '/c', 'mkdir', linkDirectory + showName + '\\Season ' + season + '\\'])
				subprocess.call(['cmd', '/c', 'mklink', linkName, name])
				found = 1

		if found:
			open(dbFile, 'a').close()