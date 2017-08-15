# Author: Barbara McGillivray, from original code by Miguel Won
# Date: 30/06/2017
# Python version: 3
# Script version: 1.0
# Script for extracting topics from cleaned letters from Hartlib archive using LDA
# from https://de.dariah.eu/tatom/working_with_text.html and https://stackoverflow.com/questions/32055071/lda-topic-modeling-input-data

# -----------------------------------------------------------------
# Initialization
# -----------------------------------------------------------------

# Import libraries

import os
from os.path import isfile, join
import math
import re
from textblob import TextBlob as tb
import csv
import numpy as np  # a conventional alias
from sklearn.feature_extraction.text import CountVectorizer
import nltk
import time
import lda

# Default parameters:

istest_default = "yes"

# User parameters:

istest = input('Is this a test? Please reply yes or not. Leave empty for default (' + str(istest_default) + ").")

# Set parameters:

if istest == "":
    istest = istest_default

# Directory and file names:

dir_in = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "lemmatization", "output"))  # relative path to data directory
dir_out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "keywords"))
file_out = "letters_keywords" + str(time.strftime("%d-%m-%Y")) + ".csv"

# create output directory if it doesn't exist:
if not os.path.exists(dir_out):
    os.makedirs(dir_out)

def xml2text(path_in):

    input = open(path_in, 'r')
    output = ""

    # parse XML:

    for line in input:
        # find words:
        word_matcher = re.match(r' +?<w .*lem=\"(.*?)\" pos=\"(.*?)\" .*xml:id=\"(.*?)\".*>(.+?)<\/w>', line)
        if word_matcher:
            lemma = word_matcher.group(1)
            pos = word_matcher.group(2)
            if pos.startswith("pn") and lemma == "i":
                lemma = "I"
            #print(lemma)
            # print output:
            output = output + str(lemma) + " "

    input.close()
    return output

# ----------------------------------------------------------------
# Topic extraction:
# ----------------------------------------------------------------

files = os.listdir(dir_in)
if istest == "yes":
    files = files[0:3]
    #files = ["31A_01_75_cleaned.xml", "9D_17_53_cleaned.xml", "46A_06_10_cleaned.xml"]

print("\n Build DTM")
tf = CountVectorizer(stop_words='english')

texts = []

for file in files:
    print("file:" + file)

    text = xml2text(os.path.join(dir_in,file))
    texts.append(tb(text))

for text in texts:

    token_dict = {}
    tokens = nltk.word_tokenize(text)

    for i in range(len(tokens)):
        token_dict[i] = tokens[i]

    len(token_dict)


print("\n Fit DTM")
tfs1 = tf.fit_transform(token_dict.values())

# set the number of topics to look for
    num = 8

    model = lda.LDA(n_topics=num, n_iter=500, random_state=1)

    #doc_id = 0
    #word_id = 2

    #print("doc id: {} word id: {}".format(doc_id, word_id))
    #print("-- count: {}".format(X[doc_id, word_id]))
    #print("-- word : {}".format(vocab[word_id]))
    #print("-- doc  : {}".format(titles[doc_id]))

    # we fit the DTM not the TFIDF to LDA
    print("\n Fit LDA to data set")
    #model.fit_transform(tfs1)
    model.fit(tfs1)

    print("\n Obtain the words with high probabilities")
    topic_word = model.topic_word_  # model.components_ also works

    print("\n Obtain the feature names")
    vocab = tf.get_feature_names()

    topic_word = model.topic_word_
    print("type(topic_word): {}".format(type(topic_word)))
    print("shape: {}".format(topic_word.shape))

    for n in range(1):
        sum_pr = sum(topic_word[n, :])
        print("topic: {} sum: {}".format(n, sum_pr))

    n = 1
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n + 1):-1]
        print('*Topic {}\n- {}'.format(i, ' '.join(topic_words)))

    doc_topic = model.doc_topic_
    print("type(doc_topic): {}".format(type(doc_topic)))
    print("shape: {}".format(doc_topic.shape))

#with open(os.path.join(dir_out, file_out), 'w', newline='') as outfile:
#    writer = csv.writer(outfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#    writer.writerow(["Letter", "Keyword", "Score"])
#    for i, blob in enumerate(texts):
#        print("Top words in " + files[i])
#        scores = {word: tfidf(word, blob, texts) for word in blob.words}
#        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
#        for word, score in sorted_words:#[:20]:
#            # exclude kewords that have numbers in them:
#            if word.isalpha():
#                print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
#                writer.writerow([files[i], word, round(score, 5)])

