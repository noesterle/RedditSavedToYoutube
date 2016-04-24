#Youtube imports 
import httplib2
import os
import sys
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
import json

CLIENT_SECRETS_FILE = "client_secrets.json"
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the Developers Console
https://console.developers.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

def youtubeLogin():
    """
    Logs into youtube using Oauth2, credentials are stored in the client_secrets.json file.
    """
    YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = "v3"

    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
    message=MISSING_CLIENT_SECRETS_MESSAGE,
    scope=YOUTUBE_READ_WRITE_SCOPE)

    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        flags = argparser.parse_args()
        credentials = run_flow(flow, storage, flags)

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        http=credentials.authorize(httplib2.Http()))
    return youtube

def createPlaylist(youtube):
    """
    If there is no playlist titled 'RedditSavedToYoutube', one is created for you.
    """
    playlists_insert_response = youtube.playlists().insert(
    part="snippet,status",
        body=dict(
            snippet=dict(
                title="RedditSavedToYoutube", #Playlist title
                description="Youtube videos found in your reddit saved posts." #Playlist description.
            ),
            status=dict(
                privacyStatus="private" #Playlist privay settings.
            )
        )
    ).execute()

    #print("New playlist id: %s" % playlists_insert_response["id"])

def read():
    """
    Read info from links.txt that is of the format title~|channel~|link.
    Returns a 2d Array containing that info.
    """
    videos=[]
    f=open('links.txt','r')
    for line in f:
        line = line.strip().split("~|")
        videos.append(line)
    return videos #2D array  [[title,channel_name,link]]

def havePlaylist(youtube):
    """
    Checks to see if you have a playlist titled 'RedditSavedToYoutube'.
    Returns the unique id or false accordingly.
    """
    results = youtube.playlists().list(part='snippet',mine=True).execute()
    for item in results['items']:
        if item['snippet']['title'] == 'RedditSavedToYoutube':
            return item['id'] #Playlist's unique id.
    return False

def videosInPlaylist(youtube,playlistID):
    """
    Finds unique id of all videos in the 'RedditSavedToYoutube' playlist. Trying to avoid duplicates.
    """
    playlist_response = youtube.playlistItems().list(part='snippet',playlistId=playlistID,maxResults=50).execute()
    playlistVideoTitle = []
    playlist_response = dict(playlist_response)
    for item in playlist_response['items']:
        playlistVideoTitle.append(item['snippet']['resourceId']['videoId'])
    return playlistVideoTitle
    
def addVideo(youtube,playlistID,videos):
    """
    Finds out which videos are in the playlist. Then searches youtube for each video that was in the links.txt.
    Trys to match the channel name and video title for each video.
    If the video is found, it is added to 'RedditSavedToYoutube' playlist.
    """
    playlistVideos = videosInPlaylist(youtube,playlistID) #Unique id of vidoes in the playlist.
    for item in videos:
        videoTitle= item[0]
        videoAuthor=item[1]
        search_response = youtube.search().list(q=videoTitle,part='id,snippet',type='video',maxResults=50).execute() #Search youtube, up to 50 videos in response.
        for item in search_response['items']:
            if item['snippet']['title'] == videoTitle and item['snippet']['channelTitle']==videoAuthor: #Check to see if this is the correct video.
                videoID=item['id']['videoId']
                kind=item['id']['kind']
                channelID=item['snippet']['channelId']
                if videoID not in playlistVideos: #If the video is not already in the playlist,
                    info={"snippet":{"playlistId":playlistID,"resourceId":{"channelId":channelID,"kind":kind,"videoId":videoID}}}
                    info2=json.dumps(info)
                    response = youtube.playlistItems().insert(part='snippet',body=json.loads(info2)).execute() #add it.

def main():
    """
    Logs into youtube.
    Reads the info from links.txt.
    Checks to see if 'RedditSavedToYoutube' playlist exists.
        Creates it, if not.
    Trys to add videos to playlist.
    
    Any errors will be written to err.txt.
    """
    try:
        youtube = youtubeLogin()
        videos = read()
        playlistID = havePlaylist(youtube)
        if not playlistID:
            createPlaylist(youtube)
            playlistID = havePlaylist(youtube)
        addVideo(youtube,playlistID,videos)
    except Exception as err:
        f = open('err.txt','a')
        f.write('YOUTUBE:\nSomething went wrong.\n',err,'\n')
        f.close()

main()
