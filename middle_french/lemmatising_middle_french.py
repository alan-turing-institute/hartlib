
# coding: utf-8

# In[28]:


# Basic variables and imports:

import codecs, csv, os, time, re, io
from os import listdir
from os.path import isfile, join
from  more_itertools import unique_everseen
from collections import Counter
from bs4 import BeautifulSoup


# directories

# change dir_in for where the new outputs are
dir_in = os.path.abspath(os.path.join(os.path.dirname(os.getcwd()), "..","hartlib","middle_french_lexicon"))
dir_letters = os.path.abspath(os.path.join(os.path.dirname(os.getcwd()), "hartlib", "middle_french","letters"))
dir_out = os.path.abspath(os.path.join(os.path.dirname(os.getcwd()), "middle_french","output"))



# In[29]:


print(dir_in)
print(dir_letters)
print(dir_out)


# In[82]:


liste_letters = os.listdir(dir_letters)
#print(liste_letters)
lexicon = open(dir_in+"/LGeRM-LexiqueMorphologique-MODE-1.0.0.xml", encoding="ISO-8859-1")
#lexicon = open(dir_in+"/LGeRM-LexiqueMorphologique-MODE-1.0.0.xml")

#lexicon_readlines = lexicon.readlines()
lexicon_read = lexicon.read()
#print(lexicon_read)
lexicon_soup = BeautifulSoup(lexicon_read,'lxml-xml')


# In[83]:


print(lexicon_soup.sponsor)

