#Copyright (C) 2018 Sneha Revanur. All rights reserved.

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweepy import API
import json
import datetime

#Twitter API credentials
consumer_key = "<Insert consumer key>"
consumer_secret = "<Insert consumer secret>"
access_key = "<Insert access key>"
access_secret = "<Insert access secret>"

auth = OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_key,access_secret)

api = API(auth)

search = "sexual assault, rape, sexual harassment, harassment, attack, catcalling, groping, domestic violence, stalking"

class listener(StreamListener):
    def on_data(self, data):
        global beenHere
        global filename
        dt = datetime.datetime.now()
        if (dt.minute%59 == 0):
            if (beenHere == False):
                filenameSuffix = str(dt.year)+'-'+str(dt.month)+'-'+str(dt.day)+'-'+str(dt.hour)+'-'+str(dt.minute)+'-'+str(dt.second)
                filename = "sexual-tweets-"+filenameSuffix+".json"
                beenHere = True
        else:
            beenHere = False
        with open(filename,"a") as file:
            file.write(data)
            return True
    def on_error(self, status):
        print (status)

beenHere = False
dt = datetime.datetime.now()
filenameSuffix = str(dt.year)+'-'+str(dt.month)+'-'+str(dt.day)+'-'+str(dt.hour)+'-'+str(dt.minute)+'-'+str(dt.second)
filename = "sexual-tweets-"+filenameSuffix+".json"

twitterStream = Stream(auth,listener())
twitterStream.filter(track=[search])

