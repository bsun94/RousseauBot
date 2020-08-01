"""
Created on Sun Jul 26 16:54:01 2020

@author: BrianSun

This is to scrape Rousseau's "On the Social Contract" from a website
"""

from bs4 import BeautifulSoup
import requests
import os
import re

class RousseauScraper:
    
    def __init__(self, startParagraph, endParagraph, twitterLimit, url):
        self.startParagraph = startParagraph
        self.endParagraph = endParagraph
        self.twitterLimit = twitterLimit
        self.url = url
        self.quotes = []
    
    # Set working directory to current folder; need to export sentences from the book into a txt later
    def dirUpdater(self):
        os.chdir(os.getcwd())
    
    # Send a request to the website; get html and use BS to parse
    def getHTML(self):
        html = requests.get(self.url).text
        soup = BeautifulSoup(html, "lxml")
        return soup
    
    # Populates the object's quotes array
    def HTMLparser(self):
        soup = self.getHTML()
        
        # Sort through all the text in the html:
        for text in soup.find_all('p'):
            try:
                paragraphNo = int(text.parent.p['id'][14:])
                
                # Only grab paragraphs in "On the Social Contract"
                if paragraphNo < self.startParagraph or paragraphNo > self.endParagraph:
                    continue
                
                elif text.string:
                    
                    # Ignore those "paragraphs" in the html that simply outline different chapters/books
                    if re.search('^(CHAPTER|BOOK)(.*):', text.string):
                        continue
                    
                    else:
                        
                        # Want to read in the document by sentence (for RousseauBot to use individually later on)
                        tempList = re.split('(?<!etc)\.\s(?!.*\")|\!', text.string)
                        for sentence in tempList:
                            
                            # When a "paragraph" is just a single sentence, re's .split() returns the sentence and a ''
                            # Also, remove overly long quotes - Twitter has char limit
                            if sentence != '' and len(sentence.strip()) < TWITTER_LIMIT:
                                self.quotes.append(sentence.strip())
                                
            except KeyError:
                
                # BS throws KeyError when <p>'s id field is blank; ignore - all paragraphs I need has an id
                continue
        
    # Write into the corpus file
    def corpusWriter(self):
        with open('corpus.txt', 'w') as file:
            for quote in self.quotes:
                file.write(quote + '\n')
    
    def runAll(self):
        self.dirUpdater()
        self.HTMLparser()
        self.corpusWriter()


# Define user-editable constants to be passed into class object as method arguments, then run
START_PARAGRAPH = 145
END_PARAGRAPH = 588
TWITTER_LIMIT = 280
URL = 'https://oll.libertyfund.org/titles/rousseau-the-social-contract-and-discourses'

corpus1 = RousseauScraper(START_PARAGRAPH, END_PARAGRAPH, TWITTER_LIMIT, URL)
corpus1.runAll()
