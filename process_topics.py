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
file_topics_in_docs = "topics-in-docs.csv"

output_file_name = "Topics_languages_dataframe.csv"
output_file_name_letters = "Topics_languages_letters_dataframe.csv"

# create output directory if it doesn't exist:
if not os.path.exists(dir_out):
    os.makedirs(dir_out)

# Today's date and time:

now = time.strftime("%c")

# Read input:

xl = pd.ExcelFile(os.path.join(dir, input_file_name))
sheets = xl.sheet_names

# sheets are: 'overview', 'EN topics', 'FR topics', 'LA topics', 'DE topics'

# ----------------------------------
# Topics and subtopics by language:
# ----------------------------------

languages = list() #list of languages
topiclanguage2microtopic = dict()  # maps each language and topic pair to the number of micro-topics that that language
subtopic2topic = dict()  # maps each (subtopic id, language) pair to the list of the topics it correponds to

for sheet in sheets:
    if sheet.endswith(' topics') and (istest != "yes" or sheet == 'EN topics'):
        #print(sheet)
        #print(language)
        #print(str(df.info()))
        #print(str(df.columns))
        #print(str(main_topics))
        #print(str(subtopics_indices))
        # map subtopics to main topics:
        df = xl.parse(sheet)
        language = sheet.replace(" topics", "")
        languages.append(language)
        df = df.fillna(0)
        main_topics = list(df.columns.values)[3:]
        subtopics_indices = df.index.values
        for topic in main_topics:
            #print(str(df[[topic]].sum()))
            topiclanguage2microtopic[topic,language] = float(df[[topic]].sum())

        for i in range(0,len(subtopics_indices)):
            for j in range(0, len(main_topics)):
                topic = main_topics[j]
                subtopic_id = int(subtopics_indices[i])
                #print("topic:"+topic)
                #print("subtopic_id:" + str(subtopic_id))
                #print("\t"+str(i) + "-" + str(j+3) + ":" + str(df.iloc[i, j+3]))
                if df.iloc[i, j+3] > 0:
                    tuple = (subtopic_id, language)
                    try:
                        list_topics = subtopic2topic(subtopic_id, language)
                        list_topics.append(topic)
                        subtopic2topic[tuple] = list_topics
                    except:
                        subtopic2topic[tuple] = [topic]

#print("***subtopic_id to topic")
#for [subtopic_id, language] in subtopic2topic:
#    print(str(subtopic_id), language, str(subtopic2topic[subtopic_id,language]))
#    print(str(type([subtopic_id, language])))
#    print(str(type(subtopic_id)), str(type(language)), str(type(subtopic2topic[subtopic_id,language])))

#print("Let us try!!!")
#print(subtopic2topic[10,'EN'])

# Print output data frame:
with open(os.path.join(dir_out, output_file_name), 'w', encoding="UTF-8") as output_file:
    file_out_writer = csv.writer(output_file, delimiter="\t")
    file_out_writer.writerow(["language", "topic", "number_subtopics"])

    for key in topiclanguage2microtopic:
        topic = key[0]
        language = key[1]
        #print(topic, "\t", language, "\t", topiclanguage2microtopic[key])
        file_out_writer.writerow([language, topic, topiclanguage2microtopic[key]])


# ----------------------------------
# Topics and number of letters:
# ----------------------------------

topiclanguage2letters = dict()  # maps each (language, subtopic) pair to the number of letters that that language
# has for that topic with score > 0.5

# Read topic extraction output per language:

for language in languages:
    print(language)
    dir_topics = os.path.join(dir, "topic_extraction", "TM_output", "TM_output_"+language, "40", "output_csv")

    topicsindocs_file = codecs.open(os.path.join(dir_topics, file_topics_in_docs), 'r', encoding='UTF-8')
    print("Reading file " + str(os.path.join(dir_topics, file_topics_in_docs)))
    first_line = topicsindocs_file.readline()
    if first_line.startswith("docId;"):
        delimiter_ch = ';'
    elif first_line.startswith("docId,"):
        delimiter_ch = ','

    topicsindocs_reader = csv.reader(topicsindocs_file, delimiter=delimiter_ch, quotechar='"')
    next(topicsindocs_reader)  # This skips the first row of the CSV file

    for row in topicsindocs_reader:
        #print("row:"+str(row))
        if len(row) > 1:
            doc_id = row[0]
            filename = row[1]
            subtopic_id = int(row[2])
            score = float(row[3])
            if score > 0.5:
                #print("subtopic_id="+str(subtopic_id), "language="+language)
                #try:
                #    print("ecco"+str(subtopic2topic([int(subtopic_id), language])))
                #except:
                #    print("this is key error for " + str(subtopic_id) + " and " + language)
                #    print("types " + str(type(subtopic_id)) + " and " + str(type(language)))
                #    print("value: " + str(subtopic2topic[int(subtopic_id), language]))
                    #print("type:" + str(type([subtopic_id, language])))
                    #print("full:"+str(subtopic2topic))
                #    if int(subtopic_id) == 10 and language == 'EN':
                #        print("yes!!!")
                #        print("Let us try!!!")
                #        print(subtopic2topic[int(subtopic_id), language])
                #    else:
                #        print("no!")
                for topic in subtopic2topic[subtopic_id, language]: # these are the topics that subtopic corresponds to
                    #print("topic:"+topic)
                    #print(str(topiclanguage2letters.keys()))
                    tuple = (topic, language)
                    if tuple in topiclanguage2letters.keys():
                        topiclanguage2letters[tuple] += 1
                    else:
                        topiclanguage2letters[tuple] = 1

    topicsindocs_file.close()

for [topic, language] in topiclanguage2letters:
    print(topic, language, str(topiclanguage2letters[topic, language]))

# Print output data frame:
with open(os.path.join(dir_out, output_file_name_letters), 'w', encoding="UTF-8") as output_file_letters:
    file_out_writer_letters = csv.writer(output_file_letters, delimiter="\t")
    file_out_writer_letters.writerow(["language", "topic", "number_letters"])

    for key in topiclanguage2letters:
        topic = key[0]
        language = key[1]
        #print(topic, "\t", language, "\t", topiclanguage2letters[key])
        file_out_writer_letters.writerow([language, topic, topiclanguage2letters[key]])

