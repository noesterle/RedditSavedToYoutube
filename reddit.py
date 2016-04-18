#Reddit imports
import requests
import requests.auth
import praw
import time


def getAccessToken(redditUsername,redditPassword,redditAppId,redditSecret,redirect,redditUser_agent):
    response = requests.post("https://www.reddit.com/api/v1/access_token",
      # client id and client secret are obtained via your reddit account
      auth = requests.auth.HTTPBasicAuth(redditAppId, redditSecret),
      # provide your reddit user id and password
      data = {"grant_type": "password", "username": redditUsername, "password": redditPassword},
      # you MUST provide custom User-Agent header in the request to play nicely with Reddit API guidelines
      headers = {"User-Agent": redditUser_agent})
    response = dict(response.json())
    return response["access_token"]

def getPraw(redditUsername,redditPassword,redditAppId,redditSecret,redirect,redditUser_agent):
        # you MUST provide custom User-Agent header in the request to play nicely with Reddit API guidelines
    r = praw.Reddit(user_agent = redditUser_agent,
        # client id and client secret are obtained via your reddit account
        oauth_client_id = redditAppId,
        oauth_client_secret = redditSecret,
        # oauth_redirect_uri isn't used for the purpose of our demo
        oauth_redirect_uri = "dummy")
    # this tells PRAW our authentication details
    r.set_access_credentials(set(["identity","save","history"]), getAccessToken(redditUsername,redditPassword,redditAppId,redditSecret,redirect,redditUser_agent))
    return r

def runBot(r):
    countertotal = 0
    counterUnknown = 0
    youtube = {}
    imgur = {}
    ted = {}
    reddit = {}
    gfycat = {}
    unknown = {}
    try:
        authenticated_user = r.get_me() #get user
        #print (authenticated_user.name, authenticated_user.link_karma) #confirm user
        saved = authenticated_user.get_saved() #get saved list.
        for x in saved:
            if isinstance(x,praw.objects.Submission):  #Checks to see if x is a submission
                if 'youtu' in x.domain:   #Checks to see if x is from youtube.com or shortened link youtu.be
                    youtube.update({x.title:x.url})
                    #x.unsave
                elif 'imgur' in x.domain:   #Checks to see if x is from imgur
                    imgur.update({x.title:x.url})
                    #x.unsave
                elif 'ted' in x.domain: #Checks to see if x is from TED
                    ted.update({x.title:x.url})
                    #x.unsave
                elif 'reddit' in x.domain or 'self.' in x.domain: #Checks to see if x is from Reddit
                    reddit.update({x.title:x.url})
                    #x.unsave
                elif 'gfycat' in x.domain:  #Checks to see if x is from gfycat
                    gfycat.update({x.title:x.url})
                    #x.unsave
                else:
                    #print(x.domain)
                    unknown.update({x.title:x.url})   #Link is from an unknown service.
            countertotal+=1
        #print("Looked through",countertotal,"items in the saved list.",counterUnknown,"were not recorded.")
        #    print(dir(x))
        return youtube
    except Exception as err:
            # do some type of logging here
            # it's better to do a named exception check in a real bots script
        print("Something went wrong. :(")
        print(err) 
    #finally:
            # wait some arbitrary amount of time before getting a refreshed access token
    #    r = getPraw()

def writeLinks(dic):
    try:
        f = open('links.txt','w')
        for item in dic:
            f.write(item+'~|'+dic[item]+'\n')
        f.close()
    except Exception as err:
        print("Something went wrong writing")
        print(err)

def readCreds():
    try:
        login = []
        f = open('redditLogin.txt','r')
        for line in f:
            line=line.strip()
            login.append(line)
        f.close()
        #print(login)
        return login
    except Exception as err:
        print("Something went wrong with reading credentials.")
        print(err)

def main():
    login = readCreds()
    youtube = runBot(getPraw(login[0],login[1],login[2],login[3],login[4],login[5]))
    #print(youtube)
    writeLinks(youtube)
    
main()