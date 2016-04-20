#Youtube imports 
import httplib2
import os
import sys
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

#Youtube info. May need spaces before and after clientid and secret. Not sure yet.
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
    playlists_insert_response = youtube.playlists().insert(
    part="snippet,status",
        body=dict(
            snippet=dict(
                title="Test Playlist",
                description="A private playlist created with the YouTube API v3"
            ),
            status=dict(
                privacyStatus="private"
            )
        )
    ).execute()

    print("New playlist id: %s" % playlists_insert_response["id"])

def read():
    links={}
    f=open('links.txt','r')
    for line in f:
        arr = line.strip().split("~|")
        #print(arr)
        #print(arr[0],len(arr[0]))
        #print(arr[1],len(arr[1]))
        links.update({str(arr[0]):str(arr[1])})
    return links

def main():
    #print(youtube)
    #print(youtubeGetAccessToken())
    youtube = youtubeLogin()
    createPlaylist(youtube)
    links = read()
    #print(links)
    
main()
