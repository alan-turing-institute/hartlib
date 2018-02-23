# Hartlib project

Code for processing the Hartlib Papers, extracting topics, and detecting semantic change. Collaboration between Barbara McGillivray, Simon Hengchen, and Robin Buning.

The script for cleaning the texts was adapted from an original script by Miguel Won.

Steps:

1) Linguistic pre-processing of letters: clean_letters_v1.7.py
2) Language identification: langid-HARTLIB.py
3) Lemmatization:
  a) English: 
    - prepare_lemmatization_v1.0.py
    - cd [folder where MorphAdorner is installed]
    - For every file:
      ./adorneme [path to output folder with double quotes] [path to input file with double quotes]
    - Prepare input for topic extraction by extracting lemmas of specific pos: select_POS.py  
  b) Latin: 
4) Topic extraction: TopicModelingTool-FR.jar
5) Topic selection/analysis: Hartlib Papers workflow.ipynb
6) Semantic change: LDA comparison.ipynb
