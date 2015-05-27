#!/usr/bin/env python3

import json
import urllib.request
import time
import pyttsx
import sys
from win32com.client import constants
import win32com.client
import twitter

#This program reads the thread titles at /r/todayilearned and shows new threads
#And some other stuff
class TIL:
	def __init__(self):
		#The threads, stored so as not to duplicate
		self.threads = []
	
		self.url = 'http://www.reddit.com/r/todayilearned/new/.json'
		#header = { 'User-Agent' : 'Just testing this bot...' }
		
		#Text to speech
		self.useT2S = True
		if self.useT2S == True:
			self.engine = pyttsx.init("sapi5", True)
		
		self.useTwitter = False
		if self.useTwitter == True:
			auth = twitter.OAuth('1868543822-YZuZmgJorclK0HBRUU7SBkDMEdw02cjE0hQgPtY', 'dz2X8SHDr2kKBJsuDFAgQ92z9J9wDdI72vaXBGPMiI',
								'OJZWc55ZMKwygCetI5tIfQ', 'FoHKSWjJE66hudQBs8IWhzdjc2qCAHX3mRxEfoH2RY8')
			self.tweet = twitter.Twitter(auth=auth)
		
		#Get a json file from the reddit API, showing the 25 newest threads in the subreddit
		self.mainLoop()
		
	#Get a json file from the reddit API, showing the 25 newest threads in the subreddit
	def requestData(self):
		request = urllib.request.Request(self.url)
		request.add_header('User-Agent', 'Just testing this bot...')
		requestData = urllib.request.urlopen(request, None)
		encoding = requestData.headers.get_content_charset()
		str_requestData = requestData.readall().decode(encoding)
		self.data = json.loads(str_requestData)
		
	#Do shit again every 30 seconds
	def mainLoop(self):
		self.addThreads()
		self.showThreads()
		while(True):
			time.sleep(30)
			self.addThreads()
			self.showThreads()
			
	#Show the found information
	def showThreads(self):
		for t in self.threads:
			if t.getUsed() == False:
				text = "\n" + t.getTitle()
				try:
					print(text)
				except:
					print("\n")
					print(bytes(text.encode('utf-8')))
					
				if self.useT2S == True:
					self.engine.say(t.getTitle())
					self.engine.runAndWait()
				
				if self.useTwitter == True:
					self.tweet.update(status="t.getTitle()")
					
				t.setUsed(True)
				
				time.sleep(2)
		
	#Identify those threads
	def addThreads(self):
		self.requestData()
		
		for thread in self.data['data']['children']:
			#for item in thread['data']:
			id = thread['data']['id']
			
			used = False
			for t in self.threads:
				if t.getID() == id:
					used = True
					break
			if used == True:
				continue
			
			title = thread['data']['title']
			title = title.replace('TIL that', '')
			title = title.replace('TIL That', '')
			title = title.replace('TIL:', '')
			title = title.replace('TIL', '')
			title = title.lstrip(' ')
			title = 'Did you know that ' + title
			
			url = 'http://www.reddit.com' + thread['data']['permalink']
			
			newThread = Topic(id, title, url)
			self.threads.append(newThread)
			
class Topic:
	def __init__(self, id, title, url):
		self.id = id
		self.title = title
		self.url = url
		self.used = False
		
	def getID(self):
		return self.id
		
	def getTitle(self):
		return self.title
		
	def getURL(self):
		return self.url
		
	def setUsed(self, used):
		self.used = used
		
	def getUsed(self):
		return self.used

if __name__ == '__main__':
	til = TIL()
