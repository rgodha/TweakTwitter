#!/usr/bin/python

import re
import sys
import string

def getStopWordList(StopWordsFile):
	#read the stopwords file and build a list
	stopWords = []

	fp = open(StopWordsFile,'r')
	line = fp.readline()
	while line:
		word = line.strip()
		stopWords.append(word)
		line = fp.readline()
	fp.close()
	return stopWords

def getTweets(ReadTweetFile, StopWordsFile):
	# Get all the stopWords
	stopWords = getStopWordList(StopWordsFile)
	#print stopWords
	
	TweetFile = open(ReadTweetFile,'r')
	for TweetDespt in TweetFile:
		TweetArr = ''
		Tweet = TweetDespt.replace("\n",'')

		#Get the tweet from the JSON data: 
		#If data is not properly formated, using try to exception and continue.
		try: 
			Tweet = TweetDespt.split(', text=')[1].split(',')[0]
		except:
			continue

		#Replace the first and last ' to blank
		Tweet = Tweet.replace('\'','')

		#Convert to lower case
		Tweet = Tweet.lower()

		#Remove www.* or https?//* 
		Tweet = re.sub('((www\.[\s]+)|(https?://[^\s]+))','',Tweet)

		#Convert @username to username
		Tweet = re.sub(r'@([^\s]+)',r'\1',Tweet)

		#Remove additional white spaces
		Tweet = re.sub('[\s]+', ' ', Tweet)
        Tweet = re.sub('^\s','',Tweet)

		#Replace #word with word
		Tweet = re.sub(r'#([^\s]+)', r'\1', Tweet)

		#Remove the numbers
		Tweet = re.sub('[\d]+','',Tweet)

		#Remove the smilies
		myre = re.compile(u'['
				u'\U0001F300-\U0001F64F'
				u'\U0001F680-\U0001F6FF'
				u'\u2600-\u26FF\u2700-\u27BF]+',
				re.UNICODE)
		myre.sub('',Tweet)

		#trim the tweet
		Tweet = Tweet.strip('\'"')
        Tweet = Tweet.strip()
	
		words = Tweet.split()
		for w in words:
			if(w in stopWords):
				continue
			else:
				TweetArr = TweetArr + ' ' +  w
	
		print TweetArr
	
	TweetFile.close()

#Starts from here. 
#Check for number of arguments passed to this file.
if len(sys.argv) != 3:
	print "Usage: python myCleanScript.py <TweetFile> <StopWordsFile>"
	sys.exit()

ReadTweetFile = sys.argv[1]
StopWordsFile = sys.argv[2]

#Call the function to
getTweets(ReadTweetFile, StopWordsFile)
