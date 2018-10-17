from __future__ import absolute_import, print_function
from time import gmtime, strftime

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json

hashtags_to_track = ['forapt', 'bolsonaro', 'haddad', 'elenao']

class AssinanteTwitter(StreamListener):
    def on_data(self, data):        
        content = json.loads(data)
        hashtags = list(filter(lambda x: x["text"].lower() in hashtags_to_track, content["entities"]["hashtags"]))

        if len(hashtags) == 0: return True
        
        hashtag = hashtags[0]["text"].lower()
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        print(time, hashtag)
        with open('hashtags.csv','a') as fd:
            fd.write("{},{}\n".format(time, hashtag))
        return True

    def on_error(self, status):
        print(status)

print("Program Started")
consumer_key=""
consumer_secret=""

access_token="329432978-"
access_token_secret="ß"

assinante = AssinanteTwitter()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

stream = Stream(auth, assinante)
stream.filter(track=map(lambda x: '#' + x, hashtags_to_track), languages=["pt"])