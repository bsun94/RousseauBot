"""
Created on Sat Jul 25 11:57:38 2020

@author: BrianSun

Tweets quotes of Rousseau from his book, "On the Social Contract"
"""

import tweepy as tw
import numpy as np
import pickle as pk
import os
import sys
import json

class RousseauTweets(object):
    
    CREDENTIALS_FILE = 'APICredentials.json'
    CORPUS_FILE = 'corpus.txt'
    PREVIOUSLY_TWEETED = 'prevIndices.txt'
    os.chdir(os.getcwd())
    
    def __init__(self):
        self.apiKey = ''
        self.apiSecret = ''
        self.accessToken = ''
        self.accessTokSecret = ''
        self.corpus = []
        self.previousIndices = []
    
    def readCredentials(self):
        """
        RousseauBot's Twitter credentials are stored in a json file, read/stored into variables below.
        Exits if not all credentials were filled-in in the APICredentials file.
        """
        with open(self.CREDENTIALS_FILE, 'r') as file:
            credDict = json.load(file)

        self.apiKey          = credDict['API Key']
        self.apiSecret       = credDict['API Secret Key']
        self.accessToken     = credDict['Access Token']
        self.accessTokSecret = credDict['Access Token Secret']
        
        for i in credDict.values():
            if not i:
                sys.exit('Empty credentials detected - please double-check the APICredentials file.')
    
    def readQuotes(self):
        """
        Read in the corpus file, containing Rousseau's "On the Social Contract" broken out into lines.
        Exits if the corpus file is not found in the current directory.
        """
        try:
            with open(self.CORPUS_FILE, 'r') as file:
                self.corpus = file.readlines()
        except:
            sys.exit("Corpus file not found or unavailable.")
    
    def readPreviousIndices(self):
        """
        Read in a pickled list, keeping track of previous lines from the corpus that was quoted in the past 10 days.
        This helps prevent the possibility of repeating the same line within 10 days. Default behaviour, if a prevIndices file
        is not found, is to create an empty array to start tracking quotes.
        """
        try:
            with open(self.PREVIOUSLY_TWEETED, 'rb') as indexFile:
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
        with open(self.PREVIOUSLY_TWEETED, 'wb') as indexFile:
            pk.dump(self.previousIndices, indexFile)
            
        return quoteToTweet
    
    def twitterPost(self, quote):
        """
        Authenticate credentials with Twitter to access RousseauBot's account. Exits if either API request or authentication fails.
        """
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
        self.readCredentials()
        self.readQuotes()
        self.readPreviousIndices()
        self.twitterPost(self.pickTrackTweet())
        

rousseau1 = RousseauTweets()
rousseau1.runAll()
