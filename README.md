# Hartlib project

Code for processing the Hartlib Papers, extracting topics, and detecting semantic change. Collaboration between Barbara McGillivray, Simon Hengchen, and Robin Buning.

Steps:

a) Linguistic pre-processing of letters:
1)	clean_letters_v1.7.py
2)	prepare_lemmatization_v1.0.py
3)	cd [folder where MorphAdorner is installed]
4)	For every file:
./adorneme [path to output folder with double quotes] [path to input file with double quotes]

b) Language identification:
1)	langid-HARTLIB.py identifies language on a line-by-line basis
2)	Rule of thumb: files smaller than 300 bytes are not proper letters but signatures and parts of other-language letters &rarr removed
