# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 11:57:38 2020

@author: Owner
"""

# import all the modules we'll need, notably tweepy to interact with Twitter API
import tweepy as tw
import numpy as np
import pickle as pk
import os

# set current folder to be the working directory
os.chdir(os.getcwd())

# initialize a list to read in the RousseauBot Twitter account's credentials; saved into a txt to avoid displaying them in the code
credList = []
with open('APICredentials.txt', 'r') as file:
    while True:
        line = file.readline()
        # get rid of newline characters in each line
        credList += [line.strip('\n')]
        # break out once finished reading file
        if not line:
            break

# search for indices where the label for each credential is stored
apiKeyInd, apiSecretInd, accTokenInd, accTokSecretInd = \
    credList.index('API Key'), credList.index('API Secret Key'), credList.index('Access Token'), credList.index('Access Token Secret')
# then get each credential as the succeeding item to each label above
apiKey, apiSecret, accessToken, accessTokSecret = \
    credList[apiKeyInd + 1], credList[apiSecretInd + 1], credList[accTokenInd + 1], credList[accTokSecretInd + 1]

# read in the corpus file, containing Rousseau's "On the Social Contract" broken out into lines
with open('corpus.txt', 'r') as file:
    corpus = file.readlines()
# read in a pickled list, keeping track of previous lines from the corpus that was quoted in the past 10 days
# this helps prevent the possibility of repeating the same line within 10 days
with open('prevIndices.txt', 'rb') as indFile:
    prevInd = pk.load(indFile)

# generate a random number such as we won't index a line from the corpus that was already indexed in the past 10 days
ind = np.random.randint(0, len(corpus)-1)
while ind in prevInd:
    ind = np.random.randint(0, len(corpus)-1)
# store current index into the previous indices list to be pickled, for keeping track going forward
prevInd.append(ind)
# just want to keep track over 10 days
if len(prevInd)>10:
    prevInd.pop(0)
# pickle the previous indices list
with open('prevIndices.txt', 'wb') as indFile:
    pk.dump(prevInd, indFile)

quoteToTweet = corpus[ind].strip('\n')

# authenticate credentials with Twitter to access RousseauBot's account
auth = tw.OAuthHandler(apiKey, apiSecret)
auth.set_access_token(accessToken, accessTokSecret)
api = tw.API(auth)

# tweet on RousseauBot's account
api.update_status(quoteToTweet)