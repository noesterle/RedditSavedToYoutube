# RedditSavedToYoutube

This consists of two python scripts.

The first script works using PRAW, which is Reddit's python API wrapper.
The Reddit script first reads through a *link.txt* file for current youtube links. It then retrieves the first 100 items in your saved list, and finds the domain of the links. At the moment, it keeps track of youtube, imgur, gfycat, and TED links. Only the youtube videos are being used. It then writes to a *link.txt* in the same folder, using the format *title*~|*channel*~|*link*. Posts that are written to *links.txt* are unsaved from your reddit saved list.
The youtube file then reads the *links.txt* and log into youtube, and those videos to a playlist. Videos that are found on youtube are removed from *link.txt*.

I can't put youtu.be links in the playlist, as reddit doesn't store the proper information for me to find them with the youtube script. They will remain in the saved list.


DEPENDANCIES:

Requires Python 3, PRAW (pip3 install praw), and several packages from Google(pip3 install --upgrade google-api-python-client).

REQUIREMENTS:

In order to run these scripts, they need access to the respective account.
For reddit, go to https://www.reddit.com/prefs/apps/ and click "create another app". You'll need the App ID and Secret.
For youtube, go to https://console.developers.google.com. In the credentials tab, you'll need to create credentials for the script in the "credential" section, and fill out the "OAuth consent screen". In the overview tab, you'll need to enable the "Youtube Data API" and "Youtube Analytics API".
Both scripts pull info from a file outside of the scripts. The reddit script reads from redditLogin.txt. The youtub script pulls from client_secret.json. Examples of both are supplied.
