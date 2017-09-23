# Hartlib project

Code for processing the Hartlib Papers, extracting topics, and detecting semantic change. Collaboration between Barbara McGillivray, Simon Hengchen, and Robin Buning.

Steps:

a) Linguistic pre-processing of letters:
1)	clean_letters_v1.7.py
2)	langid-HARTLIB.py
2)	prepare_lemmatization_v1.0.py
3)	cd [folder where MorphAdorner is installed]
4)	For every file:
./adorneme [path to output folder with double quotes] [path to input file with double quotes]
5)	select_POS.py

b) Topic extraction:
1)	TopicModelingTool-FR.jar (or MALLET, or...)

