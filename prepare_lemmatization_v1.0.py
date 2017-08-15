## -*- coding: utf-8 -*-
# Author: Barbara McGillivray
# Date: 3/05/2017
# Python version: 3
# Script version: 1.0
# Script for preparing the texts to be lemmatized by MorphAdorner

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

# Directory and file names:

#dir_in = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "selected"))  # relative path to data directory
dir_in = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "cleaned"))
dir_out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "lemmatization", "input"))  # relative path to data directory

# create output directory if it doesn't exist:
if not os.path.exists(dir_out):
    os.makedirs(dir_out)


# --------------------------
# Process letters
# --------------------------

files = [f for f in listdir(dir_in) if isfile(join(dir_in, f)) and f.startswith("1")]

for file in files:
    print("file:" + file)
    text = codecs.open(os.path.join(dir_in, file), 'r').read().replace(' & ', ' and ')#.replace("  ", " ")\
        #.replace('\r', ' ').replace("  ", " ").replace("  ", " ")
    # remove new lines from file text:


    file_out = file.replace(".txt", ".xml")
    # output = codecs.open(os.path.join(dir_out, file_out), "w", "utf-8")
    output = open(os.path.join(dir_out, file_out), "w")
    output.write("<TEI>\n")
    output.write("<text><body><div>")
    output.write(text)
    output.write("</div></body></text></TEI>")
    output.close()
