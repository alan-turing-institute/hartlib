# NATURAL LANGUAGE PROCESSING - FUZZY MATCHING OF TWO SENTENCES

# In this micro project we will see the similarity of two sentences, both intending the same meaning but are expressed in
# different voices.



# assigning a variable 'a' to first sentence
a = "If I don't buy some new music every month, I get bored with my collection."

# assigning a variable 'b' to second sentence
b = "I get bored with my collection so I buy some new music every month."

# importing NLTK library and its module to perform basic text operations

import nltk
from nltk.tokenize import WordPunctTokenizer  # tokenizer
from nltk.stem import SnowballStemmer  # stemmer
from nltk.corpus import stopwords  # stopwords

stop_words = set(stopwords.words("english"))  # setting and selecting stopwords to be in english

tokenizer = WordPunctTokenizer()  # assigning WordPunctTokenizer function to be a variable.

# This is required because we can't specify the texts inside WordPunctTokenizer() - like this --> WordPunctTokenizer(text).
# Doing this would give error. Check the below code set to understand the error -


# import nltk
# text = "Hi there! I'm going out for shopping. Would you like to come?"
# from nltk.tokenize import WordPunctTokenizer
# word_punct_tokenize = WordPunctTokenizer(text)

# TypeErrorTraceback (most recent call last)
# <ipython-input-4-440639a1a2e5> in <module>()
# ----> 1 word_punct_tokenize = WordPunctTokenizer(text)

# TypeError: __init__() takes exactly 1 argument (2 given)



stemmer = SnowballStemmer(
    'english')  # Specifying that we want to use Snowball Stemmer and we want to stem in english. Also, assigning it to a variable.

# tokenizing the sentence assigned to the variable 'a' based on the stopwords present in English within NLTK
tokens_a = [token.lower() for token in tokenizer.tokenize(a) \
            if token.lower() not in stop_words]

# fetching the output
tokens_a

["'",
 'buy',
 'new',
 'music',
 'every',
 'month',
 ',',
 'get',
 'bored',
 'collection',
 '.']

# tokenizing the sentence assigned to the variable 'b' based on the stopwords present in English within NLTK
tokens_b = [token.lower() for token in tokenizer.tokenize(b) \
            if token.lower() not in stop_words]

# fetching the output
tokens_b

['get', 'bored', 'collection', 'buy', 'new', 'music', 'every', 'month', '.']

# stemming sentence 'a' based on the 'tokens_a'
stems_a = [stemmer.stem(token) for token in tokens_a]

# fetching the output
stems_a

["'",
 u'buy',
 u'new',
 u'music',
 u'everi',
 u'month',
 ',',
 u'get',
 u'bore',
 u'collect',
 '.']

# stemming sentence 'b' based on the 'tokens_b'
stems_b = [stemmer.stem(token) for token in tokens_b]

# fetching the output
stems_b

[u'get',
 u'bore',
 u'collect',
 u'buy',
 u'new',
 u'music',
 u'everi',
 u'month',
 '.']

# calculating the similarity of the two sentence using jaccard's similarity coefficient based on their stems
jaccard_distance = len(set(stems_a).intersection(stems_b)) / float(len(set(stems_a).union(stems_b)))

# fetching the output
jaccard_distance

0.8181818181818182



# As per Jaccard's similarity coefficient, the closer the value is to 1 the more is the similarity. Hence, as per our result
# above, we can safely conclude that the two sentences are almost similar.