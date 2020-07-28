# RousseauBot
My first Twitter Bot
The two programs in this repository are behind @RousseauSays on Twitter.

The corpusBuilder script scrapes a website containing the full text from Rousseau's "On the Social Contract", which is then massaged for formatting and to retain only those quotes short enough to fit Twitter's character limit.

The RousseauBot script then reads the "corpus" built by the above and randomly selected a quote/sentence to post to Twitter. It keeps track of what it has posted the previous 10 times to avoid repetition (with certainty) posts over a short/medium period of time.
