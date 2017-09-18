## -*- coding: utf-8 -*-
# Author: Simon Hengchen, based on a script by Barbara McGillivray
# Date: 18/09/2017
# Python version: 3
# Script version: 1.0
# Script to select only a few POS from files lemmatised by Morphadorner

# Import libraries:

from __future__ import division

import codecs
import csv
import os
import time
from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup
import re
from bs4 import UnicodeDammit
import xml.etree.ElementTree as etree 
import io


# Directory and file names:


dir_in = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "hartlib", "OneDrive", "lemmatization", "cleaned_EN_output"))
dir_out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "hartlib", "OneDrive", "lemmatization", "input_TM"))  # relative path to data directory

# create output directory if it doesn't exist:
if not os.path.exists(dir_out):
    os.makedirs(dir_out)


# --------------------------
# SELECT LEMMAS ACCORDING TO TAGS
# --------------------------

# this is adverbs, verbs, nouns, adjectives according to NUPOS http://morphadorner.northwestern.edu/morphadorner/documentation/nupos/
pos_ok = ("av", "av-an", "av-c", "avc-jn", "av-n1","av-s","avs-jn","av-vvg","av-vvn","av-x","fw-fr","fw-ge","fw-la","j","j-av","jc","jc-jn","jc-vvg","jc-vvn","j-jn","jp","js","js-jn","js-vvg","js-vvn","j-vvn","j-vvg","n1","n1-an","n1-j","n2","n2-acp","n2-an","n2-av","n2-av","n2-j","n2-jn","n2-vdg","n2-vhg","n2-vvg","n2-vvn","n-jn","njp","njp2","np1","np2","np-n1","np-n2","n-vdg","n-vhg","n-vvg","n-vvn","vvb","vvbx","vvd","vvd2","vvd2x","vvdp","vvdx","vvg","vvi","vvn","vvp","vvz","vvzx") 
                

files = [f for f in listdir(dir_in) if isfile(join(dir_in, f)) ]

for file in files:
    print("file:" + file)
    file_out = file.replace(".xml", ".txt") # recreate a file but with just the POS we want
    output = open(os.path.join(dir_out, file_out), "w")

    tree = etree.parse(io.open(os.path.join(dir_in, file)))
    root = tree.getroot()
    for child in root: 
        for child2 in child:
            for child3 in child2:
                for child4 in child3:
                    for w in child4.iter('w'):
                        if w.attrib['pos'] in pos_ok:
                            output.write(w.attrib['lem']+"\n")
    output.close()
