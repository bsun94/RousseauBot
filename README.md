# RousseauBot
##### My first Twitter Bot
The two programs in this repository are behind @RousseauSays on Twitter.
_________________________________

**Package Dependencies:**
Please ensure you have the *tweepy, requests, bs4, json, pickle and numpy* python packages installed.

The corpusBuilder script scrapes a *Online Library of Liberty* webpage (https://oll.libertyfund.org/titles/rousseau-the-social-contract-and-discourses) containing the full text from Rousseau's *On the Social Contract*, which it then splits into individual sentences and cleans before exporting into a txt (called "corpus") in your current directory. **Please run this script before the RousseauBot script.**

The RousseaBot script then reads the corpus file built by the above and randomly selects a quote/sentence to post to Twitter. It keeps track of what it has posted the previous *10 times* within an array to avoid repetition (with certainty) over a short/medium time period by *pickling* this array in your current directory (which it then reads upon subsequent executions).

Please note that RousseauBot is also dependent on a JSON file containing the credentials to RousseauBot's Twitter account (API/access keys/tokens), which it reads and uses in accessing the account. *A JSON file containing empty values for all tokens/keys/secrets is shared in this repository* for users to fill in with their own credentials to try out the script. To generate/access your own credentials, please visit the Twitter developers portal.