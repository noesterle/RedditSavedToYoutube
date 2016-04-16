# RedditSavedToYoutube

This consists of two python scripts.

The first script works using PRAW, which is Reddit's python API wrapper.
The Reddit script reads through the first 25 items in your saved list, and finds the domain of the links. At the moment, it keeps track of youtube, imgur, gfycat, and TED links. Only the youtube links are being used. It then writes to a link.txt in the same folder, using the format <title>~|<link>.
The youtube file then reads the links.txt, and will add those links to a playlist.

Requires Python >2.5, Python 3, PRAW (pip install praw), gdata-python-client(https://github.com/google/gdata-python-client), TSLite(http://trevp.net/tlslite/).
Reddit script is run using Python3 and PRAw, youtube script is run using Python>2.5, gdata-client, and TSLite.
