# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 16:54:01 2020

@author: Owner
"""
# This is to scrape Rousseau's "On the Social Contract" from a website; requests imported to get html from website
# BeautifulSoup needed to parse through the html
from bs4 import BeautifulSoup
import requests
import os
import re

# Set working directory to current folder; need to export sentences from the book into a txt later
os.chdir(os.getcwd())

# Send a request to the website; get html and use BS to parse
url = 'https://oll.libertyfund.org/titles/rousseau-the-social-contract-and-discourses'
html = requests.get(url).text
soup = BeautifulSoup(html, "lxml")

# initialize quotes list
quotes = []

# sort through all the text in the html:
for text in soup.find_all('p'):
    try:
        paragraphNo = int(text.parent.p['id'][14:])
        # only paragraphs 145-588 belong to "On the Social Contract", as id'ed in the <p> tags in the html
        if paragraphNo < 145 or paragraphNo > 588:
            continue
        elif text.string:
            # ignore those "paragraphs" in the html that simply outline different chapters/books
            if re.search('^CHAPTER(.*):', text.string) or re.search('^BOOK(.*):', text.string):
                continue
            else:
                # want to read in the document by sentence (for RousseauBot to use individually later on)
                tempList = re.split('(?!etc)\.\s|\!', text.string)
                for sentence in tempList:
                    # when a "paragraph" is just a single sentence, re's .split() returns the sentence and a ''
                    #  remove these '' with .strip()
                    # also, remove overly long quotes - Twitter has char limit
                    if sentence != '' and len(sentence.strip()) < 280:
                        quotes += [sentence.strip()]
    except KeyError:
        # BS throws KeyError when <p>'s id field is blank; ignore - all paragraphs I need has an id
        continue

# write into the corpus file
with open('corpus.txt', 'w') as file:
    for quote in quotes:
        file.write(quote + '\n')