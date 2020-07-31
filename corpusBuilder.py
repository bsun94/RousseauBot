"""
Created on Sun Jul 26 16:54:01 2020

@author: BrianSun

This is to scrape Rousseau's "On the Social Contract" from a website
"""

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

quotes = []

# These paragraph numbers outline the range of "On the Social Contract" <p> tags
START_PARAGRAPH = 145
END_PARAGRAPH = 588
TWITTER_LIMIT = 280

# Sort through all the text in the html:
for text in soup.find_all('p'):
    try:
        paragraphNo = int(text.parent.p['id'][14:])
        
        # Only grab paragraphs in "On the Social Contract"
        if paragraphNo < START_PARAGRAPH or paragraphNo > END_PARAGRAPH:
            continue
        
        elif text.string:
            
            # Ignore those "paragraphs" in the html that simply outline different chapters/books
            if re.search('^(CHAPTER|BOOK)(.*):', text.string):
                continue
            
            else:
                
                # Want to read in the document by sentence (for RousseauBot to use individually later on)
                tempList = re.split('(?<!etc)\.\s(?!.*\"$)|\!', text.string)
                for sentence in tempList:
                    
                    # When a "paragraph" is just a single sentence, re's .split() returns the sentence and a ''
                    # Also, remove overly long quotes - Twitter has char limit
                    if sentence != '' and len(sentence.strip()) < TWITTER_LIMIT:
                        quotes.append(sentence.strip())
    
    except KeyError:
        
        # BS throws KeyError when <p>'s id field is blank; ignore - all paragraphs I need has an id
        continue

# Write into the corpus file
with open('corpus.txt', 'w') as file:
    for quote in quotes:
        file.write(quote + '\n')
