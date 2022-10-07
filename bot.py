import os
import json
import tweepy
from dotenv import load_dotenv
load_dotenv()


api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')
bearer_token = os.getenv('BEARER_TOKEN')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')


client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)


media = api.media_upload('images/img01.jpg', chunked=True)
media_ids = [media.media_id]
f =  open('fugitive.json')
data = json.load(f)
text = """ 
{name}
{forename}
{age} years old
From {nat}
{marks}
Crime:{chargedFor}
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
print(text)
# client.create_tweet(text= text)
# client.create_tweet(text= text, media_ids = media_ids )