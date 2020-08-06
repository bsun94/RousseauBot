"""
Created on Sun Jul 26 16:54:01 2020

@author: BrianSun

This is to scrape Rousseau's "On the Social Contract" from a website
"""

from bs4 import BeautifulSoup
import requests
import os
import re

class RousseauScraper(object):
    
    URL             = 'https://oll.libertyfund.org/titles/rousseau-the-social-contract-and-discourses'
    TWITTER_LIMIT   = 280
    START_PARAGRAPH = 145
    END_PARAGRAPH   = 588
    os.chdir(os.getcwd())
    
    def __init__(self):
        self.quotes = []
    
    def getHTML(self):
        """
        Send a request to the website; get html and use BS to parse.
        """
        html = requests.get(self.URL).text
        soup = BeautifulSoup(html, "lxml")
        return soup
    
    def HTMLparser(self):
        """
        Populates the object's quotes array.
        """
        soup = self.getHTML()
        
        # Sort through all the text in the html:
        for text in soup.find_all('p'):
            try:
                paragraphNo = int(text.parent.p['id'][14:])
                
                # Only grab paragraphs in "On the Social Contract"
                if paragraphNo < self.START_PARAGRAPH or paragraphNo > self.END_PARAGRAPH:
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
                            if sentence != '' and len(sentence.strip()) < self.TWITTER_LIMIT:
                                self.quotes.append(sentence.strip())
                                
            except KeyError:
                
                # BS throws KeyError when <p>'s id field is blank; ignore - all paragraphs I need has an id
                continue
        
    def corpusWriter(self):
        """
        Write into the corpus file.
        """
        with open('corpus.txt', 'w') as file:
            for quote in self.quotes:
                file.write(quote + '\n')
    
    def runAll(self):
        self.HTMLparser()
        self.corpusWriter()

corpus1 = RousseauScraper()
corpus1.runAll()
