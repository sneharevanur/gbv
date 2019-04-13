#Copyright (C) 2018 Sneha Revanur. All rights reserved.

import operator 
import sys
import string
import nltk
import csv
from collections import Counter
from Utils import tokenize_text
from Utils import xstr
from Utils import remove_urls
from Utils import intersect
from nltk.corpus import stopwords
from nltk import bigrams 
from nltk.stem import WordNetLemmatizer
from collections import defaultdict
 
#nltk.download('wordnet')
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via']
com = defaultdict(lambda : defaultdict(int))
stemmer = nltk.PorterStemmer()
wnl = WordNetLemmatizer()
 
intersectionMaxCount = 0
verifiedUserMaxCount = 0
tweetPlaceCountryCodeMaxCount = 0
totalMaxCount = 0

def setMaxCounts (s):
    global intersectionMaxCount
    global verifiedUserMaxCount
    global tweetPlaceCountryCodeMaxCount
    global totalMaxCount

    if (s=="harmful"):
        intersectionMaxCount = 5
        verifiedUserMaxCount = 236
        tweetPlaceCountryCodeMaxCount = 126
        totalMaxCount = 2500
    elif (s=="other"):
        intersectionMaxCount = 72
        verifiedUserMaxCount = 1214
        tweetPlaceCountryCodeMaxCount = 1214
        totalMaxCount = 2500
    elif (s=="physical"):
        intersectionMaxCount = 37
        verifiedUserMaxCount = 1032
        tweetPlaceCountryCodeMaxCount = 900
        totalMaxCount = 2500
    else:
        intersectionMaxCount = 104
        verifiedUserMaxCount = 1198
        tweetPlaceCountryCodeMaxCount = 1198
        totalMaxCount = 2500
    return

def filterFile (type, f_input, f_output):
    fout = open(f_output, 'w', newline='', encoding='utf-8')
    with open(f_input, 'rU', encoding='utf-8') as fin:
        reader = csv.DictReader(fin)

        setMaxCounts(type)

        intersectionCount = 0
        verifiedUserCount = 0
        tweetPlaceCountryCodeCount = 0
        otherCount = 0
        rowCount = 0

        onlyOnce = True

        for row in reader:
            if (onlyOnce):
                writer = csv.DictWriter(fout, fieldnames=row.keys())
                writer.writeheader()
                onlyOnce = False

            text = row['text_text']
            #print('text='+text)
            if (text.startswith('RT')):
                continue

            tweet_lang = row['tweet_lang']
            #print('tweet_lang='+tweet_lang)
            if (not tweet_lang.startswith('en')):
                continue

            text_hashtags_count = row['text_hashtags_count']
            #print('text_hashtags_count='+text_hashtags_count)
            if (int(text_hashtags_count) > 3):
                continue

            text_symbols_count = row['text_symbols_count']
            #print('text_symbols_count='+text_symbols_count)
            if (int(text_symbols_count) > 3):
                continue

            text_user_mentions_count = row['text_user_mentions_count']
            #print('text_user_mentions_count='+text_user_mentions_count)
            if (int(text_user_mentions_count) > 3):
                continue

            text_urls_count = row['text_urls_count']
            #print('text_urls_count='+text_urls_count)
            if (int(text_urls_count) > 3):
                continue

            text_media_count = row['text_media_count']
            #print('text_media_count='+text_media_count)
            if (int(text_media_count) > 3):
                continue

            user_followers_count = row['user_followers_count']
            #print('user_followers_count='+user_followers_count)
            if (int(user_followers_count) < 10):
                continue

            user_friends_count = row['user_friends_count']
            #print('user_friends_count='+user_friends_count)
            if (int(user_friends_count) < 10):
                continue

            user_listed_count = row['user_listed_count']
            #print('user_listed_count='+user_listed_count)
            if (int(user_listed_count) < 5):
                continue

            text = text.replace('SNE_COMMA', ',')
            text = text.replace('SNE_QUOTE', '\"')
            text = text.replace('SNE_LF', '\n')

            # Create a list with all the terms
            terms_all = [term for term in tokenize_text(text, True)]
            #print("terms_all="+xstr(terms_all))

            # Count terms only (no hashtags, no mentions)
            terms_without_hashtags_mentions = [term for term in terms_all if term not in stop and not term.startswith(('#', '@'))] 
            #print("terms_without_hashtags_mentions="+xstr(terms_without_hashtags_mentions))

            # terms only (no URLs)
            terms_without_urls = [remove_urls(term) for term in terms_without_hashtags_mentions]
            #print("terms_without_urls="+xstr(terms_without_urls))

            # non empty and more than one character long terms only
            terms_only = [term for term in terms_without_urls if term != "" and len(term) > 1]
            #print("terms_only="+xstr(terms_only))

            if (len(terms_only) < 5):
                continue

            user_verified = row['user_verified']
            #print('user_verified='+user_verified)

            tweet_place_country_code = row['tweet_place_country_code']
            #print('tweet_place_country_code='+tweet_place_country_code)

            #both need to be valid
            if (user_verified=='TRUE' and tweet_place_country_code!="" and intersectionCount<intersectionMaxCount):
                intersectionCount = intersectionCount + 1
                rowCount = rowCount + 1
                #write intersection records
                writer.writerow(row)
                continue
        
            #only verified users
            if (user_verified=='TRUE' and tweet_place_country_code=="" and verifiedUserCount<verifiedUserMaxCount):
                verifiedUserCount = verifiedUserCount + 1
                rowCount = rowCount + 1
                #write verified user only  records
                writer.writerow(row)
                continue

            #only non-empty tweet_place country code
            if (user_verified=='FALSE' and tweet_place_country_code!="" and tweetPlaceCountryCodeCount<tweetPlaceCountryCodeMaxCount):
                tweetPlaceCountryCodeCount = tweetPlaceCountryCodeCount + 1
                rowCount = rowCount + 1
                #write non-empty tweet place country code only  records
                writer.writerow(row)
                continue
 
            if (otherCount<totalMaxCount-intersectionMaxCount-verifiedUserMaxCount-tweetPlaceCountryCodeMaxCount):
                otherCount = otherCount + 1
                rowCount = rowCount + 1
                #write remaining records
                writer.writerow(row)
                continue
        
            if (rowCount>=totalMaxCount):
                break

        print('-----------')
        print('intersectionMaxCount='+xstr(intersectionMaxCount))
        print('verifiedUserMaxCount='+xstr(verifiedUserMaxCount))
        print('tweetPlaceCountryCodeMaxCount='+xstr(tweetPlaceCountryCodeMaxCount))
        print('totalMaxCount='+xstr(totalMaxCount))

        print('intersectionCount='+xstr(intersectionCount))
        print('verifiedUserCount='+xstr(verifiedUserCount))
        print('tweetPlaceCountryCodeCount='+xstr(tweetPlaceCountryCodeCount))
        print('otherCount='+xstr(otherCount))
        print('rowCount='+xstr(rowCount))
        fout.close()
    return

#filterFile ("harmful", "./data/preprocessed/harmful-tweets-preprocessed-spl.csv", "./data/preprocessed/harmful-tweets-preprocessed-condensed-v2.csv")
#filterFile ("other", "./data/preprocessed/other-tweets-preprocessed-spl.csv", "./data/preprocessed/other-tweets-preprocessed-condensed-v2.csv")
#filterFile ("physical", "./data/preprocessed/physical-tweets-preprocessed.csv", "./data/preprocessed/physical-tweets-preprocessed-condensed-v2.csv")
#filterFile ("sexual", "./data/preprocessed/sexual-tweets-preprocessed.csv", "./data/preprocessed/sexual-tweets-preprocessed-condensed-v2.csv")
#filterFile ("sexual2", "./data/preprocessed/sexual2-tweets-preprocessed.csv", "./data/preprocessed/sexual2-tweets-preprocessed-condensed-v2.csv")

filterFile ("harmful", "./data/preprocessed/harmful-tweets-preprocessed-condensed.csv", "./data/preprocessed/harmful-tweets-preprocessed-condensed-v2.csv")
filterFile ("other", "./data/preprocessed/other-tweets-preprocessed-condensed.csv", "./data/preprocessed/other-tweets-preprocessed-condensed-v2.csv")
filterFile ("physical", "./data/preprocessed/physical-tweets-preprocessed-condensed.csv", "./data/preprocessed/physical-tweets-preprocessed-condensed-v2.csv")
filterFile ("sexual", "./data/preprocessed/sexual-tweets-preprocessed-condensed.csv", "./data/preprocessed/sexual-tweets-preprocessed-condensed-v2.csv")
#filterFile ("sexual2", "./data/preprocessed/sexual2-tweets-preprocessed-condensed.csv", "./data/preprocessed/sexual2-tweets-preprocessed-condensed-v2.csv")
