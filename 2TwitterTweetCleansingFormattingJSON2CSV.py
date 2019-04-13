#Copyright (C) 2018 Sneha Revanur. All rights reserved.

import json
import sys
import glob
from Utils import tokenize_text
from Utils import xstr

def preprocess_text_characters (text):
    text = xstr(text)
    text = text.translate(non_bmp_map)
    text = text.replace(',', 'SNE_COMMA')
    text = text.replace('\n', 'SNE_LF')
    text = text.replace('\"', 'SNE_QUOTE')    
    return text

def preprocess_user_header (fw):
    fw.write(
        '"'+xstr('user_id_str')+'"'+delimiter+
        '"'+xstr('user_name')+'"'+delimiter+
        '"'+xstr('user_screen_name')+'"'+delimiter+
        '"'+xstr('user_location')+'"'+delimiter+
        '"'+xstr('user_profile_location')+'"'+delimiter+
        '"'+xstr('user_description')+'"'+delimiter+
        '"'+xstr('user_url')+'"'+delimiter+
        '"'+xstr('user_entities')+'"'+delimiter+
        '"'+xstr('user_protected')+'"'+delimiter+
        '"'+xstr('user_followers_count')+'"'+delimiter+
        '"'+xstr('user_friends_count')+'"'+delimiter+
        '"'+xstr('user_listed_count')+'"'+delimiter+
        '"'+xstr('user_created_at')+'"'+delimiter+
        '"'+xstr('user_favorites_count')+'"'+delimiter+
        '"'+xstr('user_utc_offset')+'"'+delimiter+
        '"'+xstr('user_time_zone')+'"'+delimiter+
        '"'+xstr('user_geo_enabled')+'"'+delimiter+
        '"'+xstr('user_verified')+'"'+delimiter+
        '"'+xstr('user_statuses_count')+'"'+delimiter+
        '"'+xstr('user_lang')+'"'+delimiter+
        '"'+xstr('user_contributers_enabled')+'"'+delimiter+
        '"'+xstr('user_profile_image_url')+'"'+delimiter+
        '"'+xstr('user_default_profile')+'"'+delimiter+
        '"'+xstr('user_follow_request_sent')+'"'+delimiter
        )
    return

def preprocess_user (s, fw):
    name = preprocess_text_characters(s.get('name'))
    location = preprocess_text_characters(s.get('location'))
    description = preprocess_text_characters(s.get('description'))
    
    fw.write(
        '"'+xstr(s.get('id_str'))+'"'+delimiter+
        '"'+name+'"'+delimiter+
        '"'+xstr(s.get('screen_name'))+'"'+delimiter+
        '"'+location+'"'+delimiter+
        '"'+xstr(s.get('profile_location'))+'"'+delimiter+
        '"'+description+'"'+delimiter+
        '"'+xstr(s.get('url'))+'"'+delimiter+
        '"'+xstr(s.get('entities'))+'"'+delimiter+
        '"'+xstr(s.get('protected'))+'"'+delimiter+
        '"'+xstr(s.get('followers_count'))+'"'+delimiter+
        '"'+xstr(s.get('friends_count'))+'"'+delimiter+
        '"'+xstr(s.get('listed_count'))+'"'+delimiter+
        '"'+xstr(s.get('created_at'))+'"'+delimiter+
        '"'+xstr(s.get('favorites_count'))+'"'+delimiter+
        '"'+xstr(s.get('utc_offset'))+'"'+delimiter+
        '"'+xstr(s.get('time_zone'))+'"'+delimiter+
        '"'+xstr(s.get('geo_enabled'))+'"'+delimiter+
        '"'+xstr(s.get('verified'))+'"'+delimiter+
        '"'+xstr(s.get('statuses_count'))+'"'+delimiter+
        '"'+xstr(s.get('lang'))+'"'+delimiter+
        '"'+xstr(s.get('contributers_enabled'))+'"'+delimiter+
        '"'+xstr(s.get('profile_image_url'))+'"'+delimiter+
        '"'+xstr(s.get('default_profile'))+'"'+delimiter+
        '"'+xstr(s.get('follow_request_sent'))+'"'+delimiter
        )
    return

def preprocess_coordinates_header (fw):
    return

def preprocess_coordinates (s, fw):
    print(json.dumps(s, indent=4)) # pretty-print
    return

def preprocess_text_header (fw):
    fw.write(
        '"'
        +xstr('text_text')+
        '"'+delimiter+'"'+xstr('text_hashtags_count')+
        '"'+delimiter+'"'+xstr('text_symbols_count')+
        '"'+delimiter+'"'+xstr('text_user_mentions_count')+
        '"'+delimiter+'"'+xstr('text_urls_count')+
        '"'+delimiter+'"'+xstr('text_media_count')+
        '"'+delimiter
        )
    return

def preprocess_text (text, entities, fw):
    text = preprocess_text_characters(text)

    hashtagsCount = 0
    symbolsCount = 0
    user_mentionsCount = 0
    urlsCount = 0
    mediaCount = 0
    hashtags = entities.get('hashtags')
    if (hashtags != None):
        hashtagsCount = len(hashtags)
    symbols = entities.get('symbols')
    if (symbols != None):
        symbolsCount = len(symbols)
    user_mentions = entities.get('user_mentions')
    if (user_mentions != None):
        user_mentionsCount = len(user_mentions)
    urls = entities.get('urls')
    if (urls != None):
        urlsCount = len(urls)
    media = entities.get('media')
    if (media != None):
        mediaCount = len(media)
    fw.write(
        '"'
        +text+
        '"'+delimiter+'"'+xstr(hashtagsCount)+
        '"'+delimiter+'"'+xstr(symbolsCount)+
        '"'+delimiter+'"'+xstr(user_mentionsCount)+
        '"'+delimiter+'"'+xstr(urlsCount)+
        '"'+delimiter+'"'+xstr(mediaCount)+
        '"'+delimiter
        )
    return

def preprocess_extended_tweet (s, fw):
    text = preprocess_text_characters(s.get('full_text'))

    entities = s.get('entities')
    hashtagsCount = 0
    symbolsCount = 0
    user_mentionsCount = 0
    urlsCount = 0
    mediaCount = 0
    hashtags = entities.get('hashtags')
    if (hashtags != None):
        hashtagsCount = len(hashtags)
    urls = entities.get('urls')
    if (urls != None):
        urlsCount = len(urls)
    user_mentions = entities.get('user_mentions')
    if (user_mentions != None):
        user_mentionsCount = len(user_mentions)
    symbols = entities.get('symbols')
    if (symbols != None):
        symbolsCount = len(symbols)
    media = entities.get('media')
    if (media != None):
        mediaCount = len(media)
    fw.write(
        '"'
        #+xstr(text.translate(non_bmp_map))+
        +text+
        '"'+delimiter+'"'+xstr(hashtagsCount)+
        '"'+delimiter+'"'+xstr(urlsCount)+
        '"'+delimiter+'"'+xstr(user_mentionsCount)+
        '"'+delimiter+'"'+xstr(symbolsCount)+
        '"'+delimiter+'"'+xstr(mediaCount)+
        '"'+delimiter
        )
    return

def preprocess_tweet_header (fw):
    fw.write(
        '"'
        +xstr('tweet_created_at')+
        '"'+delimiter+'"'+xstr('tweet_id_str')+
        '"'+delimiter+'"'+xstr('tweet_source')+
        '"'+delimiter+'"'+xstr('tweet_in_reply_to_status_id')+
        '"'+delimiter+'"'+xstr('tweet_in_reply_to_status_id_str')+
        '"'+delimiter+'"'+xstr('tweet_in_reply_to_user_id')+
        '"'+delimiter+'"'+xstr('tweet_in_reply_to_user_id_str')+
        '"'+delimiter+'"'+xstr('tweet_in_reply_to_screen_name')+
        '"'+delimiter+'"'+xstr('tweet_place_name')+
        '"'+delimiter+'"'+xstr('tweet_place_full_name')+
        '"'+delimiter+'"'+xstr('tweet_place_country_code')+
        '"'+delimiter+'"'+xstr('tweet_place_country')+
        '"'+delimiter+'"'+xstr('tweet_is_quote_status')+
        '"'+delimiter+'"'+xstr('tweet_retweet_count')+
        '"'+delimiter+'"'+xstr('tweet_favorite_count')+
        '"'+delimiter+'"'+xstr('tweet_favorited')+
        '"'+delimiter+'"'+xstr('tweet_retweeted')+
        '"'+delimiter+'"'+xstr('tweet_possibly_sensitive')+
        '"'+delimiter+'"'+xstr('tweet_lang')+
        '"'+delimiter+'"'+xstr('tweet_truncated')+
        '"'+delimiter+'"'+xstr('tweet_quoted_status_id_str')+
        '"'+delimiter
        )
    
    #preprocess_coordinates_header(fw)
    
    preprocess_user_header(fw)
    
    preprocess_text_header(fw)
    return

def preprocess_tweet (s, fw):
    truncated = xstr(s.get('truncated'))
    retweeted_status = xstr(s.get('retweeted_status'))
    quoted_status = xstr(s.get('quoted_status'))

    source = xstr(s.get('source'))
    if (source != ""):
        start = source.index(">", 0)
        end = source.index("<", start+1)
        source = source[start+1:end]
        source = preprocess_text_characters(source)

    place_name = ""
    place_full_name = ""
    place_country_code = ""
    place_country = ""
    place = s.get('place')
    if (place != None):
        place_name=xstr(place.get('name'))
        place_full_name=xstr(place.get('full_name'))
        place_country_code=xstr(place.get('country_code'))
        place_country=xstr(place.get('country'))
    
    fw.write(
        '"'
        +xstr(s.get('created_at'))+
        '"'+delimiter+'"'+xstr(s.get('id_str'))+
        '"'+delimiter+'"'+source+
        '"'+delimiter+'"'+xstr(s.get('in_reply_to_status_id'))+
        '"'+delimiter+'"'+xstr(s.get('in_reply_to_status_id_str'))+
        '"'+delimiter+'"'+xstr(s.get('in_reply_to_user_id'))+
        '"'+delimiter+'"'+xstr(s.get('in_reply_to_user_id_str'))+
        '"'+delimiter+'"'+xstr(s.get('in_reply_to_screen_name'))+
        '"'+delimiter+'"'+place_name+
        '"'+delimiter+'"'+place_full_name+
        '"'+delimiter+'"'+place_country_code+
        '"'+delimiter+'"'+place_country+
        '"'+delimiter+'"'+xstr(s.get('is_quote_status'))+
        '"'+delimiter+'"'+xstr(s.get('retweet_count'))+
        '"'+delimiter+'"'+xstr(s.get('favorite_count'))+
        '"'+delimiter+'"'+xstr(s.get('favorited'))+
        '"'+delimiter+'"'+xstr(s.get('retweeted'))+
        '"'+delimiter+'"'+xstr(s.get('possibly_sensitive'))+
        '"'+delimiter+'"'+xstr(s.get('lang'))+
        '"'+delimiter+'"'+xstr(s.get('truncated'))+
        '"'+delimiter+'"'+xstr(s.get('quoted_status_id_str'))+
        '"'+delimiter
        )
    
    #preprocess_coordinates(s['coordinates'], fw)
    
    preprocess_user(s['user'], fw)
    
    if (truncated == 'False'):
        preprocess_text(s['text'], s['entities'], fw)
    else:    
        preprocess_extended_tweet(s['extended_tweet'], fw)

    #if (retweeted_status != ""):
    #    print("In Retweeted Status")
    #    preprocess_tweet(s['retweeted_status'], fw)
        
    #if (quoted_status != ""):
    #    print("In Quoted Status")
    #    preprocess_tweet(s['quoted_status'], fw)
    return

def preprocess_file (f_input, f_output, onlyOnce):
    count=0
    file_tweet_count=0
    start_index=3435
    max_count=3439
    global total_tweet_count

    print('--------')
    print('input='+f_input, ' output='+f_output);

    f_write = open(f_output, 'a', encoding='utf-8')
    if (onlyOnce):
        preprocess_tweet_header(f_write)
        f_write.write('\n')

    with open(f_input, 'r', newline='\r\n') as f:
        for line in f:
            #if (count < max_count):
            #    if (count >= start_index):
                    tweet = json.loads(line) # load it as Python dict
                    # to avoid running into 'limit' responses
                    if 'text' in tweet:
                        preprocess_tweet(tweet, f_write)
                        f_write.write('\n')
                        file_tweet_count = file_tweet_count+1
                    count = count+1
    f_write.close()

    total_tweet_count = total_tweet_count + file_tweet_count
    print('file tweet count='+xstr(file_tweet_count))
    return

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
delimiter = ','
total_tweet_count = 0
onlyOnce=True
filenamePrefix='sexual'
filenamePrefix2=0
filenamePrefix2_str=""

files = glob.glob("../data/"+filenamePrefix+"*.json")
for f in files:
    preprocess_file(f, filenamePrefix+filenamePrefix2_str+'-tweets-preprocessed.csv', onlyOnce)
    onlyOnce=False
    if (int(total_tweet_count/750000) > filenamePrefix2):
        filenamePrefix2=int(total_tweet_count/750000)+1
        filenamePrefix2_str=xstr(filenamePrefix2)
        onlyOnce=True
        
    
print('--------')
print('total tweet count='+xstr(total_tweet_count))
