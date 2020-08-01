"""
Created on Sat Jul 25 11:57:38 2020

@author: BrianSun

Tweets quotes of Rousseau from his book, "On the Social Contract"
"""

# Import libraries, especially tweepy to interact with Twitter API
import tweepy as tw
import numpy as np
import pickle as pk
import os
import sys
import json

class RousseauTweets:
    
    def __init__(self, credentialFile, corpusFile, previousTweets):
        self.credentialFile = credentialFile
        self.corpusFile = corpusFile
        self.previousTweets = previousTweets
        self.apiKey = ''
        self.apiSecret = ''
        self.accessToken = ''
        self.accessTokSecret = ''
        self.corpus = []
        self.previousIndices = []
    
    # Set current folder to be the working directory
    def updateDir(self):
        os.chdir(os.getcwd())
    
    # RousseauBot's Twitter credentials are stored in a json file, read/stored into variables below
    def readCredentials(self):
        with open(self.credentialFile, 'r') as file:
            credDict = json.load(file)

        self.apiKey          = credDict['API Key']
        self.apiSecret       = credDict['API Secret Key']
        self.accessToken     = credDict['Access Token']
        self.accessTokSecret = credDict['Access Token Secret']
    
    # Read in the corpus file, containing Rousseau's "On the Social Contract" broken out into lines
    def readQuotes(self):
        try:
            with open(self.corpusFile, 'r') as file:
                self.corpus = file.readlines()
        except:
            sys.exit("Corpus file not found or unavailable.")
    
    # Read in a pickled list, keeping track of previous lines from the corpus that was quoted in the past 10 days
    # This helps prevent the possibility of repeating the same line within 10 days
    def readPreviousIndices(self):
        try:
            with open(self.previousTweets, 'rb') as indexFile:
                self.previousIndices = pk.load(indexFile)
        except:
            self.previousIndices = []
    
    
    def pickTrackTweet(self):
        
        # Generate a random number such as we won't index a line from the corpus that was already indexed in the past 10 days
        index = np.random.randint(0, len(self.corpus)-1)
        while index in self.previousIndices:
            index = np.random.randint(0, len(self.corpus)-1)
        
        # Store current index into the previous indices list to be pickled, for keeping track going forward
        self.previousIndices.append(index)
        
        # Just want to keep track over 10 days
        if len(self.previousIndices) > 10:
            self.previousIndices.pop(0)
        
        quoteToTweet = self.corpus[index].strip('\n')
        
        # Pickle the previous indices list
        with open(self.previousTweets, 'wb') as indexFile:
            pk.dump(self.previousIndices, indexFile)
            
        return quoteToTweet
    
    # Authenticate credentials with Twitter to access RousseauBot's account
    def twitterAuth(self, quote):
        try:
            auth = tw.OAuthHandler(self.apiKey, self.apiSecret)
        except:
            sys.exit("API request rejected by Twitter.")
                
        try:
            auth.set_access_token(self.accessToken, self.accessTokSecret)
        except:
            sys.exit("Authentication failed.")
        
        api = tw.API(auth)
        api.update_status(quote)
    
    def runAll(self):
        self.updateDir()
        self.readCredentials()
        self.readQuotes()
        self.readPreviousIndices()
        self.twitterAuth(self.pickTrackTweet())
        
# Define user-updatable constants for files containing credentials, quotes, previous tweets; then run
CREDENTIALS_FILE = 'APICredentials.json'
CORPUS_FILE = 'corpus.txt'
PREVIOUSLY_TWEETED = 'prevIndices.txt'

rousseau1 = RousseauTweets(CREDENTIALS_FILE, CORPUS_FILE, PREVIOUSLY_TWEETED)
rousseau1.runAll()
