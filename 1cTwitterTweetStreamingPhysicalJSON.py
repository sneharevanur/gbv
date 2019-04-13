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

search = "woman dragged, women dragged, girl dragged, girls dragged, female dragged, females dragged, woman hit, women hit, girl hit, girls hit, female hit, females hit, woman beat up, women beat up, girl beat up, girls beat up, female beat up, females beat up, woman shoved, women shoved, girl shoved, girls shoved, female shoved, females shoved, woman pushed, women pushed, girl pushed, girls pushed, female pushed, females pushed, woman kicked, women kicked, girl kicked, girls kicked, female kicked, females kicked, woman slapped, women slapped, girl slapped, girls slapped, female slapped, females slapped, woman burned, women burned, girl burned, girls burned, female burned, females burned, woman acid attack, women acid attack, girl acid attack, girls acid attack, female acid attack, females acid attack, woman violence, women violence, girl violence, girls violence, female violence, females violence, woman aggression, women aggression, girl aggression, girls aggression, female aggression, females aggression, woman bullying, women bullying, girl bullying, girls bullying, female bullying, females bullying"

class listener(StreamListener):
    def on_data(self, data):
        global beenHere
        global filename
        dt = datetime.datetime.now()
        if (dt.minute%59 == 0):
            if (beenHere == False):
                filenameSuffix = str(dt.year)+'-'+str(dt.month)+'-'+str(dt.day)+'-'+str(dt.hour)+'-'+str(dt.minute)+'-'+str(dt.second)
                filename = "physical-tweets-"+filenameSuffix+".json"
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
filename = "physical-tweets-"+filenameSuffix+".json"

twitterStream = Stream(auth,listener())
twitterStream.filter(track=[search])

