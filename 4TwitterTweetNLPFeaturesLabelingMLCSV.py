#Copyright (C) 2018 Sneha Revanur. All rights reserved.

import operator 
import sys
import string
import nltk
import csv
import enchant
from collections import defaultdict
from Utils import tokenize_text
from Utils import xstr
from Utils import remove_urls
from Utils import intersect
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.collocations import *
from nltk.sentiment.util import * 
from nltk.classify import NaiveBayesClassifier
from nltk.classify import DecisionTreeClassifier
from nltk.sentiment import SentimentAnalyzer

#nltk.download('wordnet')
punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via']
wnl = WordNetLemmatizer()
 
# create a list of search words - individual, bigrams and ngrams across Harmful, Other, Physical and Sexual classes
harmful_search_unigrams = ['child', 'marriage', 'trafficking', 'genital', 'mutilation', 'honor', 'killing', 'bride', 'burning', 'infanticide']
harmful_search_bigrams = [('child', 'marriage'), ('forced', 'marriage'), ('sex', 'trafficking'), ('genital', 'mutilation'), ('honor', 'killing'), ('bride', 'burning'), ('female', 'infanticide')]

other_search_unigrams = ['trolling', 'cursing', 'cussing', 'swearing', 'abusive', 'sexist', 'offensive', 'misogynistic', 'spammer']
other_search_bigrams = [('abusive', 'language')]

physical_search_unigrams = ['domestic', 'violence', 'woman', 'dragged', 'girl', 'female', 'hit', 'beat', 'up', 'shoved', 'pushed', 'kicked', 'slapped', 'burned', 'acid', 'attack', 'aggression', 'bullying']
physical_search_bigrams = [('domestic', 'violence'), ('woman', 'dragged'), ('girl', 'dragged'), ('female', 'dragged'), ('woman', 'hit'), ('girl', 'hit'), ('female', 'hit'), ('woman', 'shoved'), ('girl', 'shoved'), ('female', 'shoved'), ('woman', 'pushed'), ('girl', 'pushed'), ('female', 'pushed'), ('woman', 'kicked'), ('girl', 'kicked'), ('female', 'kicked'), ('woman', 'slapped'), ('girl', 'slapped'), ('female', 'slapped'), ('woman', 'burned'), ('girl', 'burned'), ('female', 'burned'), ('woman', 'violence'), ('girl', 'violence'), ('female', 'violence'), ('woman', 'aggression'), ('girl', 'aggression'), ('female', 'aggression'), ('woman', 'bullying'), ('girl', 'bullying'), ('female', 'bullying')]
physical_search_trigrams = [('woman', 'beat', 'up'), ('girl', 'beat', 'up'), ('female', 'beat', 'up'), ('woman', 'acid', 'attack'), ('girl', 'acid', 'attack'), ('female', 'acid', 'attack')]

sexual_search_unigrams = ['sexual', 'assault', 'rape', 'harassment', 'catcalling', 'groping', 'stalking']
sexual_search_bigrams = [('sexual', 'assault'), ('sexual', 'harassment')]

def get_terms (fname, max_row_count):
    with open(fname, 'rU', encoding='utf-8') as f:
        reader = csv.DictReader(f, dialect='excel')
        total_terms_en_singles_only = []
        for row in reader:
            #print(row)
       
            #tweet_id_str = row['tweet_id_str']
            #if (tweet_id_str != '965058314802483000' and tweet_id_str != '962927689144258000' and tweet_id_str != '963249789851717000' and tweet_id_str != '962919417221976000' and tweet_id_str != '963068587496927000'):
            #    continue

            text = row['text_text']
            text = text.replace('SNE_COMMA', ',')
            text = text.replace('SNE_QUOTE', '\"')
            text = text.replace('SNE_LF', '\n')
            #print('-----------')
            #print(tweet_id_str)
            #print(text)

            # Create a list with all the terms
            terms_all = [term for term in tokenize_text(text, True)]
            #print("terms_all="+xstr(terms_all))

            # Count terms only (no stopwords, no hashtags, no mentions)
            terms_without_stopwords_hashtags_mentions = [term for term in terms_all if term not in stop and not term.startswith(('#', '@'))] 
            #print("terms_without_stopwords_hashtags_mentions="+xstr(terms_without_stopwords_hashtags_mentions))

            # terms only (no URLs)
            terms_without_urls = [remove_urls(term) for term in terms_without_stopwords_hashtags_mentions]
            #print("terms_without_urls="+xstr(terms_without_urls))

            # non empty and more than one character long terms only
            terms_only = [term for term in terms_without_urls if term != "" and len(term) > 1]
            #print("terms_only="+xstr(terms_only))

            # convert plurals to singulars
            terms_singulars_only = [wnl.lemmatize(term) for term in terms_only]
            #print("terms_singulars_only="+xstr(terms_singulars_only))

            # create a list of terms by removing redundancy, equivalent to Document Frequency (for a single Tweet)
            terms_singles_only = set()
            terms_singles_only  = [term for term in terms_singulars_only if not (term in terms_singles_only or terms_singles_only.add(term))]
            #print("terms_singles_only="+xstr(terms_singles_only))

            d = enchant.Dict("en_US")
            terms_en_singles_only = [term for term in terms_singles_only if d.check(term)]
            #print("terms_en_singles_only="+xstr(terms_en_singles_only))

            total_terms_en_singles_only.append(terms_en_singles_only)
            if (len(total_terms_en_singles_only) >= max_row_count):
                break
    return total_terms_en_singles_only

def get_labels (fname, max_row_count):
    with open(fname, 'rU', encoding='utf-8') as f_class_label:
        reader = csv.DictReader(f_class_label, dialect='excel')
        total_tweet_class = []
        for tweet_class_row in reader:
            #tweet_id_str = tweet_class_row['\ufefftweet_id_str']
            #if (tweet_id_str != '965058314802483000' and tweet_id_str != '962927689144258000' and tweet_id_str != '963249789851717000' and tweet_id_str != '962919417221976000' and tweet_id_str != '963068587496927000'):
            #    continue

            tweet_class = tweet_class_row['tweet_classification']
            total_tweet_class.append(tweet_class)
            if (len(total_tweet_class) >= max_row_count):
                break
    return total_tweet_class

def perform_ml (total_terms, training_data, testing_data, type):
    #print("total_terms="+xstr(total_terms))
    #print("traning_tweets="+xstr(training_data))
    #print("testing_tweets="+xstr(testing_data))

    sentim_analyzer = SentimentAnalyzer()
    all_words = sentim_analyzer.all_words([terms for terms in total_terms])

    # use unigram feats from class specific unigram lists
    unigram_feats = []
    if (type == "nlp_terms"):
        unigram_feats = sentim_analyzer.unigram_word_feats(all_words, min_freq=4)
    else:
        unigram_feats = harmful_search_unigrams+other_search_unigrams+physical_search_unigrams+sexual_search_unigrams
    #print("unigram_feats="+xstr(unigram_feats))
    print(str(len(unigram_feats)))

    # use bigram feats from class specific bigram lists
    bigram_feats = []
    if (type == "nlp_terms"):
        bigram_measures = nltk.collocations.BigramAssocMeasures()
        bi_finder = BigramCollocationFinder.from_words(all_words)
        bi_finder.apply_freq_filter(3)
        bigram_feats = bi_finder.nbest(bigram_measures.pmi, -1)
        #bigram_feats = bi_finder.nbest(bigram_measures.pmi, 100)
        #bigram_feats = bi_finder.nbest(bigram_measures.chi_sq, -1)
        #bigram_feats = bi_finder.nbest(bigram_measures.likelihood_ratio, 100)
    else:
        bigram_feats = harmful_search_bigrams+other_search_bigrams+physical_search_bigrams+sexual_search_bigrams
    #print("bigram_feats="+xstr(bigram_feats))
    print(str(len(bigram_feats)))

    sentim_analyzer.add_feat_extractor(extract_unigram_feats, unigrams=unigram_feats)
    sentim_analyzer.add_feat_extractor(extract_bigram_feats, bigrams=bigram_feats)

    training_set = sentim_analyzer.apply_features(training_data)
    test_set = sentim_analyzer.apply_features(testing_data)

    #print("training_set="+xstr(training_set))
    print(str(len(training_set)))
    #print("test_set="+xstr(test_set))
    print(str(len(test_set)))

    test_data_only = []
    test_labels_only = []
    for test_data_row in test_set:
        test_data_only.append(test_data_row[0])
        test_labels_only.append(test_data_row[1])

    trainer = NaiveBayesClassifier.train
    classifier = sentim_analyzer.train(trainer, training_set)
    for key,value in sorted(sentim_analyzer.evaluate(test_set).items()):
        print('{0}: {1}'.format(key, value))

    nltk_pred_labels = classifier.classify_many(test_data_only)

    cm = nltk.ConfusionMatrix(test_labels_only, nltk_pred_labels)
    print(cm.pretty_format(sort_by_count=True, show_percents=False, truncate=9))

    informative_features = classifier.show_most_informative_features(25)
    print("Most Informative Features="+xstr(informative_features))

    return

total_terms_harmful = get_terms('./data/preprocessed/harmful-tweets-preprocessed-condensed-v3.csv', 1000)
total_terms_other = get_terms('./data/preprocessed/other-tweets-preprocessed-condensed-v3.csv', 1000)
total_terms_physical = get_terms('./data/preprocessed/physical-tweets-preprocessed-condensed-v3.csv', 1000)
total_terms_sexual = get_terms('./data/preprocessed/sexual-tweets-preprocessed-condensed-v3.csv', 1000)
total_terms = total_terms_harmful + total_terms_other + total_terms_physical + total_terms_sexual

total_labels_harmful = get_labels('./data/preprocessed/harmful-tweets-labeled.csv', 1000)
total_labels_other = get_labels('./data/preprocessed/other-tweets-labeled.csv', 1000)
total_labels_physical = get_labels('./data/preprocessed/physical-tweets-labeled.csv', 1000)
total_labels_sexual = get_labels('./data/preprocessed/sexual-tweets-labeled.csv', 1000)

training_tweets_harmful = list(zip(total_terms_harmful, total_labels_harmful))
training_tweets_other = list(zip(total_terms_other, total_labels_other))
training_tweets_physical = list(zip(total_terms_physical, total_labels_physical))
training_tweets_sexual = list(zip(total_terms_sexual, total_labels_sexual))

total_tweets = training_tweets_harmful + training_tweets_other + training_tweets_physical + training_tweets_sexual
random.shuffle(total_tweets)

training_tweets = [tweet for tweet in total_tweets[:1600]] + [tweet for tweet in total_tweets[2400:4000]]
testing_tweets = [tweet for tweet in total_tweets[1600:2400]]

#training_tweets = [tweet for tweet in total_tweets[:2]] + [tweet for tweet in total_tweets[3:5]]
#testing_tweets = [tweet for tweet in total_tweets[2:3]]

#perform_ml (total_terms, training_tweets, testing_tweets, "nlp_terms")
perform_ml (total_terms, training_tweets, testing_tweets, "search_terms")
