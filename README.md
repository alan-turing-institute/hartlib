# Hartlib project

Code for processing the Hartlib Papers, extracting topics, and detecting semantic change. Collaboration between Barbara McGillivray, Simon Hengchen, and Robin Buning.

The script for cleaning the texts was adapted from an original script by Miguel Won.

Steps:

a) Linguistic pre-processing of letters:
1)	clean_letters_v1.7.py
2)	langid-HARTLIB.py
2)	prepare_lemmatization_v1.0.py
3)	Lemmatization:
  a) English: cd [folder where MorphAdorner is installed]
    	For every file:
      ./adorneme [path to output folder with double quotes] [path to input file with double quotes]
  b) Latin: 
5)	select_POS.py

b) Topic extraction:
1)	TopicModelingTool-FR.jar (or MALLET, or...)

c) Topic selection/analysis:
1) Hartlib Papers workflow.ipynb
2) LDA comparison.ipynb
