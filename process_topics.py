## -*- coding: utf-8 -*-
# Author: Barbara McGillivray
# Date: 31/10/2019
# Python version: 3
# Code for analysing the topics from the Hartlib Papers in the different languages

# Import libraries:

import csv
import os
import time
from openpyxl import load_workbook
import pandas as pd
import codecs


# Default parameters:

istest_default = "yes"

encoding = "utf-8"

# User parameters:

istest = input('Is this a test? Please reply yes or not. Leave empty for default (' + str(istest_default) + ").")


# Set parameters:

if istest == "":
    istest = istest_default

# Directory and file names:

dir = "/Users/bmcgillivray/Documents/OneDrive/The Alan Turing Institute/The Alan Turing Institute/Hartlib Papers - Documents/Topics"
dir_out = os.path.join(dir, "analysis", "output")

input_file_name = "Topics_overview.xlsx"
output_file_name = "Topics_languages_dataframe.csv"

# create output directory if it doesn't exist:
if not os.path.exists(dir_out):
    os.makedirs(dir_out)

# Today's date and time:

now = time.strftime("%c")

# Read input:

xl = pd.ExcelFile(os.path.join(dir, input_file_name))
sheets = xl.sheet_names

# sheets are: 'overview', 'EN topics', 'FR topics', 'LA topics', 'DE topics'
languages = list() #list of languages
topiclanguage2microtopic = dict()  # maps each language and topic pair to the number of micro-topics that that language
# has for that topic
for sheet in sheets:
    if sheet.endswith(' topics'):
        if istest != "yes" or sheet == 'EN topics':
            df = xl.parse(sheet)
            #print(sheet)
            language = sheet.replace(" topics", "")
            languages.append(language)
            #print(language)
            #print(str(df.info()))
            #print(str(df.columns))
            df = df.fillna(0)
            main_topics = list(df.columns.values)[3:]
            #print(str(main_topics))
            for topic in main_topics:
                #print(topic)
                #print(str(df[[topic]]))
                #print(str(df[[topic]].sum()))
                topiclanguage2microtopic[topic,language] = float(df[[topic]].sum())

# Print output data frame:
with open(os.path.join(dir_out, output_file_name), 'w', encoding="UTF-8") as output_file:
    file_out_writer = csv.writer(output_file, delimiter="\t")
    file_out_writer.writerow(["language", "topic", "number_topics"])

    for key in topiclanguage2microtopic:
        topic = key[0]
        language = key[1]
        print(topic, "\t", language, "\t", topiclanguage2microtopic[key])
        file_out_writer.writerow([language, topic, topiclanguage2microtopic[key]])
