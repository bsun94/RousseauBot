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

# Set current folder to be the working directory
os.chdir(os.getcwd())

# RousseauBot's Twitter credentials are stored in a json file, read/stored into variables below
with open('APICredentials.json', 'r') as file:
    credDict = json.load(file)

apiKey          = credDict['API Key']
apiSecret       = credDict['API Secret Key']
accessToken     = credDict['Access Token']
accessTokSecret = credDict['Access Token Secret']

# Read in the corpus file, containing Rousseau's "On the Social Contract" broken out into lines
try:
    with open('corpus.txt', 'r') as file:
        corpus = file.readlines()
except:
    sys.exit("Corpus file not found or unavailable.")

# Read in a pickled list, keeping track of previous lines from the corpus that was quoted in the past 10 days
# This helps prevent the possibility of repeating the same line within 10 days
try:
    with open('prevIndices.txt', 'rb') as indexFile:
        prevIndex = pk.load(indexFile)
except:
    prevIndex = []

# Generate a random number such as we won't index a line from the corpus that was already indexed in the past 10 days
index = np.random.randint(0, len(corpus)-1)
while index in prevIndex:
    index = np.random.randint(0, len(corpus)-1)
    
# Store current index into the previous indices list to be pickled, for keeping track going forward
prevIndex.append(index)

# Just want to keep track over 10 days
if len(prevIndex) > 10:
    prevIndex.pop(0)
    
# Pickle the previous indices list
with open('prevIndices.txt', 'wb') as indexFile:
    pk.dump(prevIndex, indexFile)

quoteToTweet = corpus[index].strip('\n')

# Authenticate credentials with Twitter to access RousseauBot's account
try:
    auth = tw.OAuthHandler(apiKey, apiSecret)
except:
    sys.exit("API request rejected by Twitter.")

try:
    auth.set_access_token(accessToken, accessTokSecret)
except:
    sys.exit("Authentication failed.")
    
api = tw.API(auth)

# Tweet on RousseauBot's account
api.update_status(quoteToTweet)
