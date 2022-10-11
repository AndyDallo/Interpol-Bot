import os
import json
import tweepy
from dotenv import load_dotenv
load_dotenv()

# TWITTER API KEYS
api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')
bearer_token = os.getenv('BEARER_TOKEN')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

# SET UP TWITTER CLIENT
client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

#UPLOAD IMAGE
media = api.media_upload('images/img01.jpg', chunked=True)
media_ids = [media.media_id]

# READ JSON FILES
f =  open('fugitive.json')
data = json.load(f)


#TWEET CONTENT
text = """ 
{name}
{forename}
{age} years old
From {nat}
Mark: {marks}
Crime: {chargedFor}
Search by {chargedBy}
""".format(
    name= data['name'],
    forename= data['forename'],
    age= data['age'],
    nat= data['nat'],
    marks= data['marks'],
    chargedFor= data['charges']['for'],
    chargedBy= data['charges']['by']
    )

# PUBLISH TWEET
client.create_tweet(text= text, media_ids = media_ids )