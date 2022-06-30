# OofnanBot
import tweepy
import os
import time
from dotenv import load_dotenv
load_dotenv()

# Authenticating to Twitter
def createApi():
    '''Function to connect and authenticate to the Twitter API'''

    # Getting the env variables
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CONSUMER_KEY")
    CONSUMER_KEY = os.getenv("CONSUMER_KEY")
    CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
    ACCESS_KEY = os.getenv("ACCESS_KEY")
    ACCESS_SECRET= os.getenv("ACCESS_SECRET")

    # Authorizing
    auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Checking the connection
    try:
        api.verify_credentials()
        print("Authorized!")
    except:
        print("An Error occurred during authentication")

    return api

api = createApi()

def infoAboutMe(user):
    '''Function that returns a string with user's name, description and location.'''
    location_present = True # Flag Variable to check if the user has publicly set their location.
    
    if user.location == '':
        location_present = False

    if location_present:
        user_details = f" 𝐍𝐚𝐦𝐞: {user.name} \n 𝐃𝐞𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧: {user.description} \n 𝐋𝐨𝐜𝐚𝐭𝐢𝐨𝐧: {user.location}"
    else:
        user_details = f" 𝐍𝐚𝐦𝐞: {user.name} \n 𝐃𝐞𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧: {user.description} \n 𝐋𝐨𝐜𝐚𝐭𝐢𝐨𝐧: Unknown 🤫"
    
    return user_details


def getLastSeenID(file_name):
    fobj = open(file_name, 'r')
    last_seen_id = int(fobj.read().strip())
    fobj.close()
    return last_seen_id

def storeLastSeenID(last_seen_id, file_name):
    fobj = open(file_name, 'w')
    fobj.write(str(last_seen_id))
    fobj.close()
    return


def replyToTweets():

    # Getting the last_seen_ID
    last_seen_id = getLastSeenID("last_seen_id.txt")

    # Grabbing the mentions timeline
    timeline = api.mentions_timeline(since_id = last_seen_id, tweet_mode='extended') # Extended to allow for a tweet's full_text
    
    for tweet in reversed(timeline):


        print(f"Tweet ID: {tweet.id} - {tweet.user.name} said {tweet.full_text}")

        storeLastSeenID(tweet.id, "last_seen_id.txt")
        # 1541814691629977600
        if '#helloworld' in tweet.full_text.lower():

            reply_tweet = " #HelloWorld back to you!! " + "@" + tweet.user.screen_name
            api.update_status(reply_tweet, in_reply_to_status_id = tweet.id)
            print("A Hello World Response Has Been Sent.")

        elif '#aboutme' in tweet.full_text.lower():
            reply_tweet = infoAboutMe(tweet.user) + '\n' + "@" + tweet.user.screen_name
            api.update_status(reply_tweet, in_reply_to_status_id = tweet.id)
            print("An About Me Response Has Been Sent.")



if __name__=="__main__":
    while True:
        replyToTweets()
        time.sleep(15)
