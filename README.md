# RousseauBot
My first Twitter Bot
The two programs in this repository are behind @RousseauSays on Twitter.

The corpusBuilder script scrapes a Online Library of Liberty webpage (https://oll.libertyfund.org/titles/rousseau-the-social-contract-and-discourses) containing the full text from Rousseau's "On the Social Contract", which it then splits into individual sentences and cleans before exporting into a txt (called "corpus") in your current directory. This script is notably dependent on the requests and bs4 modules.

This corpus.txt file serves as an input to the RousseauBot script.

The RousseauBot script is dependent on a JSON file containing the credentials to RousseauBot's Twitter account, which it reads and uses in accessing the account (API/access keys/tokens). The JSON file shared in this repository contains empty values for all tokens/keys/secrets, meant for any user to fill in with their own credentials. The script then reads the corpus file built by the above and randomly selects a quote/sentence to post to Twitter. It keeps track of what it has posted the previous 10 times to avoid repetition (with certainty) posts over a short/medium period of time by creating and exporting a pickle of an array into your current directory (which it then reads upon subsequent executions). This script is notably dependent on the tweepy, json and numpy modules.