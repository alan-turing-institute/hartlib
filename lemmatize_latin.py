## -*- coding: utf-8 -*-
# Author: Barbara McGillivray
# Date: 23/02/2018
# Python version: 3
# Script version: 1.0
# Script for lemmatizing the Latin letters in Hartlib papers

# Import modules:

import codecs
import os
from os import listdir
from os.path import isfile, join
from cltk.stem.lemma import LemmaReplacer
from cltk.stem.latin.j_v import JVReplacer
from nltk.tokenize import sent_tokenize
import re

# Directory and file names:

dir = os.path.join("/Users", "bmcgillivray", "Documents", "OneDrive", "The Alan Turing Institute", "Hartlib Papers - Documents", "lemmatization", "la")
dir_in = os.path.join("/Users", "bmcgillivray", "Documents", "OneDrive", "The Alan Turing Institute", "Hartlib Papers - Documents", "cleaned-la")
dir_out = os.path.join(dir, "output")

# create output directory if it doesn't exist:
if not os.path.exists(dir_out):
    os.makedirs(dir_out)


# Initialize lemmatizer:

lemmatizer = LemmaReplacer('latin')

# Read input files:

print(str((dir_in)))
files = [f for f in listdir(dir_in) if isfile(join(dir_in, f)) and f.endswith('_la')]

for file in files:

    print("file:" + file)
    text = codecs.open(os.path.join(dir_in, file), 'r').read()

    file_out = file.replace(".txt_la", "_la_lemmas.txt")
    # output = codecs.open(os.path.join(dir_out, file_out), "w", "utf-8")
    output = open(os.path.join(dir_out, file_out), "w")


    lemmatized_sentences = list()

    # Sentence segmentation:

    sentences = sent_tokenize(text)

    # Separate punctuation mark:

    for i in range(0, len(sentences)):
        sentences[i] = re.sub(r'^(.*?)(.)$', r'\1 \2', sentences[i]).lower()

        lemmatized_sentence = " ".join(lemmatizer.lemmatize(sentences[i]))

        # Write to output files:
        output.write(lemmatized_sentence)