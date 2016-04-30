#Reddit imports
import requests
import requests.auth
import praw
import time


def getAccessToken(redditUsername,redditPassword,redditAppId,redditSecret,redirect,redditUser_agent):
    """
    Get a reddit access token.
    """
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
    """
    Initializes object to interact with reddit.
    """
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
    """
    Access saved list.
    Sort items into lists based on domain.
    """
    countertotal = 0
    counterUnknown = 0
    youtube = []
    imgur = []
    ted = []
    reddit = []
    gfycat = []
    unknown = []
    try:
        authenticated_user = r.get_me() #get user
        #print (authenticated_user.name, authenticated_user.link_karma) #confirm user
        saved = authenticated_user.get_saved(limit=100)#limit=100) #get saved list.
        for x in saved:
            if isinstance(x,praw.objects.Submission):  #Checks to see if x is a submissiona
                #print(x.domain,x.title)
                if 'youtube' in x.domain:   #Checks to see if x is from youtube.com or shortened link youtu.be
                    youtube.append([x.media['oembed']['title'],x.media['oembed']['author_name'],x.url])
                    x.unsave()
                elif 'imgur' in x.domain:   #Checks to see if x is from imgur
                    imgur.append([x.title,x.url])
                    #x.unsave()
                elif 'ted' in x.domain: #Checks to see if x is from TED
                    ted.append([x.title,x.url])
                    #x.unsave()
                elif 'reddit' in x.domain or 'self.' in x.domain: #Checks to see if x is from Reddit
                    reddit.append([x.title,x.url])
                    #x.unsave()
                elif 'gfycat' in x.domain:  #Checks to see if x is from gfycat
                    gfycat.append([x.title,x.url])
                    #x.unsave()
                else:
                    #print(x.domain)
                    unknown.append([x.title,x.url])   #Link is from an unknown service.
                    counterUnknown+=1
            countertotal+=1
        #print("Looked through",countertotal,"items in the saved list.",counterUnknown,"were not recorded.")
        return youtube
    except Exception as err:
        f = open('err.txt','a')
        f.write("REDDIT:\n"+time.asctime()+"\nSomething went wrong running the bot.\n"+str(err)+'\n')  
        f.close()

def writeLinks(videos):
    """
    Write video info to file in form of title~|channel~|link.
    """
    try:
        f = open('links.txt','w')
        for item in videos:
            f.write(item[0]+'~|'+item[1]+'~|'+item[2]+'\n')
        f.close()
    except Exception as err:
        f = open('err.txt','a')
        f.write("REDDIT:\n"+time.asctime()+"\nSomething went wrong writing the links to file.\n",err,'\n')
        f.close()

def readCreds():
    """
    Read credentials found in redditLogin.txt to log into reddit.
    """
    try:
        login = []
        f = open('redditLogin.txt','r')
        for line in f:
            line=line.strip()
            login.append(line)
        f.close()
        return login
    except Exception as err:
        f = open('err.txt','a')
        f.write("REDDIT:\n"+time.asctime()+"\nSomething went wrong with reading credentials.\n",err,'\n')
        f.close()

def readLinks():
    """
    Read video info from file.
    """
    try:
        youtubeList=[]
        f = open('links.txt','r')
        for line in f:
            line=line.strip().split("~|")
            youtubeList.append(line)
        f.close()
        return youtubeList
    except Exception as err:
        f = open('err.txt','a')
        f.write("REDDIT:\n"+time.asctime()+"\nSomething went wrong with reading the links.\n"+err+"\n")
        f.close()

def main():
    """
    Read video info from file.
    Log into reddit.
    Get and sort saved items.
    Add new videos to the list.
    Write new info to file.
    """
    videos = readLinks()
    login = readCreds()
    youtube = runBot(getPraw(login[0],login[1],login[2],login[3],login[4],login[5]))
    if len(youtube)>0:
        for item in videos:
            if item not in youtube:
                youtube.append(item)
        writeLinks(youtube)
    
main()
