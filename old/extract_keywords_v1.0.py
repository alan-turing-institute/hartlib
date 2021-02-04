# Author: Barbara McGillivray, from original code by Miguel Won
# Date: 10/04/2017
# Python version: 3
# Script version: 1.0
# Script for extracting keywords from cleaned letters from Hartlib archive

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

# Define functions

# This function computes the term frequency, which is the number of times a word appears in a document blob,
# normalized by dividing by the total number of words in blob.
# We use TextBlob for breaking up the text into words and getting the word counts:
def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

# This function returns the number of documents containing a word:
def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)

# This function computes the inverse document frequency, which measures how common a word is among
# all documents in bloblist
def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

# This function computes the TF-IDF score:
def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

# This function converts the XML text from MorphAdorner's lemmatization output to running text contaiing the lemmas one after the other:

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
# Keyword extraction:
# ----------------------------------------------------------------

files = os.listdir(dir_in)
if istest == "yes":
    #files = [files[0]]
    files = ["31A_01_75_cleaned.xml", "9D_17_53_cleaned.xml", "46A_06_10_cleaned.xml"]

texts = []

for file in files:
    print("file:" + file)

    text = xml2text(os.path.join(dir_in,file))
    texts.append(tb(text))

with open(os.path.join(dir_out, file_out), 'w', newline='') as outfile:
    writer = csv.writer(outfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["Letter", "Keyword", "Score"])
    for i, blob in enumerate(texts):
        print("Top words in " + files[i])
        scores = {word: tfidf(word, blob, texts) for word in blob.words}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        for word, score in sorted_words:#[:20]:
            # exclude kewords that have numbers in them:
            if word.isalpha():
                print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
                writer.writerow([files[i], word, round(score, 5)])