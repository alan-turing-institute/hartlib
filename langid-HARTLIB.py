#!/usr/bin/python
# -*- coding: utf-8 -*-



# Simon Hengchen - shengche@ulb.ac.be - http://homepages.ulb.ac.be/~shengche


import codecs
import re
import io
import os,glob
import langid
from multiprocessing import Pool 
from langid.langid import LanguageIdentifier, model


identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)
langid.set_languages(['en'])  

def get_path(dossier):
	return (os.path.join(dossier, f)
		for f in os.listdir(dossier)
		if 'txt' in f)

# "files/correct/"+chemin[10:]+"	

def langiding(chemin):

	f = io.open(chemin,"r",encoding="utf8")
	fen = io.open("../cleaned-en/"+chemin[11:]+"_en","w",encoding="utf8") # one file for each language
	

	en = 0 # we initialize counters, this allows to delete empty files

	f = f.readlines()



	for line in f:
		langue = identifier.classify(line)
							
		if langue[0] == 'en' and langue[1] > 0.85: # the probablity score needs to be of at least 0.85
			fen.write(line)
			en = en +1



	if en == 0: # if any of these files has an empty counter (i.e. no line has been written), we remove it
		os.remove("../cleaned-en/"+chemin[11:]+"_en")


if __name__ == '__main__': # we call the main program, specify the place where the files are stored
	dossier = glob.glob('../cleaned/')
	dossier = dossier[0]
	print dossier
	liste_fichiers = get_path(dossier)
	pool = Pool(1)  # specify number of cores you want this to run on
	pool.map(langiding, liste_fichiers)
	pool.close() 
	pool.join()


