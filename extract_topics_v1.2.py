# Author: Barbara McGillivray, from original code by Miguel Won
# Date: 30/06/2017
# Python version: 3
# Script version: 1.0
# Script for extracting topics from cleaned letters from Hartlib archive using LDA
# from https://www.analyticsvidhya.com/blog/2016/08/beginners-guide-to-topic-modeling-in-python/

# -----------------------------------------------------------------
# Initialization
# -----------------------------------------------------------------

# Import libraries

import os
import re
import string
import time

from gensim import corpora, models
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from langdetect import detect
from stop_words import get_stop_words

# Default parameters:

istest_default = "yes"

# User parameters:

istest = input('Is this a test? Please reply yes or not. Leave empty for default (' + str(istest_default) + ").")

# Set parameters:

if istest == "":
    istest = istest_default

# Directory and file names:

dir_in = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "lemmatization", "output"))  # relative path to data directory
dir_out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "topic_extraction", "input"))
file_out = "letters_keywords" + str(time.strftime("%d-%m-%Y")) + ".csv"

# create output directory if it doesn't exist:
if not os.path.exists(dir_out):
    os.makedirs(dir_out)

def xml2text(path_in):

    input = open(path_in, 'r', encoding = 'utf-8')
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

#https://radimrehurek.com/gensim/tut1.html !!!!!!

exclude = set(string.punctuation)
lemma = WordNetLemmatizer()

def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized


files = os.listdir(dir_in)
if istest == "yes":
    files = files[0:10]
    #files = ["19B_11_122_cleaned.xml", "19B_11_126_cleaned.xml", "19B_11_134_cleaned.xml"]

# Clean texts:

#stoplist = set('for a of the and to in be have it me I it have et und'.split())
languages = ['en', 'fr', 'de', 'la']
stoplist_en = stopwords.words('english')
stoplist_en = stoplist_en + ['Mr', 'mr', 'I', 'a', 'may', 'shall', 'the']
stoplist_fr = get_stop_words('fr')
stoplist_de = get_stop_words('de')
stoplist_la = ['ab', 'ac', 'ad', 'adhic', 'aliqui', 'aliquis', 'an', 'ante', 'apud', 'at', 'atque', 'aut', 'autem', 'cum', 'cur', 'de', 'deinde', 'dum', 'ego', 'enim', 'ergo', 'es', 'est', 'et', 'etiam', 'etsi', 'ex', 'fio', 'haud', 'hic', 'iam', 'idem', 'igitur', 'ille', 'in', 'infra', 'inter', 'interim', 'ipse', 'is', 'ita', 'magis', 'modo', 'mox', 'nam', 'ne', 'nec', 'necque', 'neque', 'nisi', 'non', 'nos', 'o', 'ob', 'per', 'possum', 'post', 'pro', 'quae', 'quam', 'quare', 'qui', 'quia', 'quicumque', 'quidem', 'quilibet', 'quis', 'quisnam', 'quisquam', 'quisque', 'quisquis', 'quo', 'quoniam', 'sed', 'si', 'sic', 'sive', 'sub', 'sui', 'sum', 'super', 'suus', 'tam', 'tamen', 'trans', 'tu', 'tum', 'ubi', 'uel', 'uero', 'unus', 'ut']
stoplist_la = stoplist_la + ['sit', 'eorum', 'penes', 'ut', 'mihi', 'quod', 'te', 'et']
stoplists = {'en': stoplist_en, 'fr': stoplist_fr, 'de': stoplist_de, 'la': stoplist_la}

for l in languages:
    output_stop = open(os.path.join(dir_out, "stoplist_" + l + ".txt"), "w")
    for w in stoplists[l]:
        output_stop.write(w + "\n")
    output_stop.close()

texts = []
for file in files:
    #f = open(os.path.join(dir_in, file), 'r')
    if file.endswith(".xml") and not file.startswith("test"):
        print(file)
        cleaned_tokens_text = []
        file_text = xml2text(os.path.join(dir_in, file))

        lemmas_text = file_text.split()

        # Detect language:
        language = detect(file_text)
        if language not in ['en', 'fr', 'de']:
            language = 'la'
        print(file)
        print(language)

        output = open(os.path.join(dir_out, language, file.replace(".xml", "_lemmas.txt")), "w")

        # Exclude stoplist:
        for t in lemmas_text:
            output.write(t + " ")
            if t not in stoplists[language]:
                cleaned_tokens_text.append(t)


        texts.append(cleaned_tokens_text)

#print("Texts:")
#print(texts)
#doc_clean = [clean(doc).split() for doc in files]

# ------------------------------------
# Prepare the Document-Term Matrix
# ------------------------------------

# Create the term dictionary of our courpus, where every unique term is assigned an index.

dictionary = corpora.Dictionary(texts)
#print("Dictionary:")
#print(dictionary)

# Define corpus:

corpus = [dictionary.doc2bow(text) for text in texts]
#print("Corpus:")
#print(corpus)

# Create transformation:

tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model
corpus_tfidf = tfidf[corpus] # apply transformation to the corpus


# Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.

#doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

# -------------------------------------
# Run the LDA model
# -------------------------------------

ldamodel = models.LdaModel(corpus, id2word=dictionary, num_topics=10)
#print(ldamodel)

# Creating the object for LDA model using gensim library
#Lda = gensim.models.ldamodel.LdaModel

# Running and Trainign LDA model on the document term matrix.
#ldamodel = Lda(doc_term_matrix, num_topics=3, id2word = dictionary, passes=50)


#print("\n Build DTM")
#tf = CountVectorizer(stop_words='english')

# ------------------------------------
# Print the results
# ------------------------------------

print(ldamodel.print_topics(num_topics=10, num_words=10))
#print(ldamodel.print_topics(2))

# select top 50 words for each of the 20 LDA topics
top_words = [[word for _, word in ldamodel.show_topic(topicno, topn=50)] for topicno in range(ldamodel.num_topics)]
print(top_words)

for i in  ldamodel.show_topics():
    print(i[0], i[1])

for i in ldamodel.show_topics(formatted=False,num_topics=ldamodel.num_topics,num_words=len(ldamodel.id2word)):
    print(i)
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

