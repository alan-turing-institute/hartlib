## -*- coding: utf-8 -*-
# Author: Barbara McGillivray, from original code by Miguel Won
# Date: 18/02/2017
# Python version: 3
# Script version: 1.5
# Changes from version 1.1: edited rules and added new rules following thorough testing of letters;
# added new tests in unit_tests2.txt
# Changes from version 1.2: generalized pattern matching for annotations_sq within square and angular brackets
# Changes from version 1.3: loop over italic patterns within square brackets replaced the conditions on
# three_italic_texts/two_talic_texts/one_italic_text
# Changes from version 1.4: loop over italic patterns within angular brackets replaced the conditions on
# three_italic_texts/two_talic_texts/one_italic_text

# Import libraries:

from __future__ import division

import codecs
import csv
import os
import time
from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup
import re
from bs4 import UnicodeDammit

# Default parameters:

istest_default = "yes"

# User parameters:

# Python 2.7:
#istest = raw_input("Is this a test? Please reply yes or not. Leave empty for default (" + str(istest_default) + ").")
#num_test = raw_input("Which test are you interested in? Leave empty if you want all tests.")
# Python 3:
istest = input('Is this a test? Please reply yes or not. Leave empty for default (' + str(istest_default) + ").")
num_test = input("Which test are you interested in? Leave empty if you want all tests.")

# Directory and file names:

#dir_in = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "selected"))  # relative path to data directory
dir_in = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Hartlib Papers 2nd edition"))  # relative path to data directory
dir_out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "cleaned"))
dir_tests = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "test_data"))
tests_file = "unit_tests2.txt"
test_output_file = "testing_results_" + str(time.strftime("%d-%m-%Y")) + ".tsv"
test_output_file_summary = "testing_results_summary.csv"

# create output directory if it doesn't exist:
if not os.path.exists(dir_out):
    os.makedirs(dir_out)

# Set parameters:

if istest == "":
    istest = istest_default

# Today's date and time:

now = time.strftime("%c")

# --------------------------
# Unit tests
# --------------------------

unit_tests = dict()  # maps a string to its desired output
unit_tests_input = list()  # lists all input tests

# with codecs.open(os.path.join(dir_tests, tests_file), 'r', "utf-8") as tests:
with open(os.path.join(dir_tests, tests_file), 'r') as tests:
    next(tests)
    tests_reader = csv.reader(tests, delimiter='\t')

    for row in tests_reader:
        # print "0:"+row[0]
        # print "1:"+row[1]
        # input = row[0].replace(u'\xa0', ' ').replace("  ", " ")
        input = row[0].replace("  ", " ")
        # output = row[1].replace(u'\xa0', ' ').replace("  ", " ")
        output = row[1].replace("  ", " ")
        unit_tests[input] = output  # .encode("utf-8")
        unit_tests_input.append(input)

# ---------------------------------------------
# Function for cleaning a string of HTML text:
# ---------------------------------------------

list_text_missing = ["illeg. word", "illeg. word/s", "illeg.word", "illeg.", "word illeg.", "blank", "words missing: MS torn",
                     "words missing:", "word missing:", "word missing: MS torn", "words missing",
                     'word missing? MS torn', "word missing, MS torn",
                     "illeg.word, MS damaged", "overwritten in another hand: letters/numerals illeg.", "illeg.",
                     "above address, another hand: numerals? illeg.", "letters illeg."
                     #"one word deleted", "Greek word deleted", "word/s deleted", "3 words deleted", "2 words deleted",
                     #'illeg. words deleted', "letters deleted","two words deleted", "deletion", "2 letters deleted",
                    #'number? deleted', "letter deleted", "letter deleted?", "word deleted"
                     ]


removed_what_follows_sq = ["H alters from", "H alters", "altered from ", "altered from", "? altered from", "H. alters",
                 "H alters from ?", "overwritten:", "overwritten in another hand?:", "overwritten in another hand:",
                "left and right margins, Hartlib:"
                           #"left margin:", "left column:", "right column:", "right margin:", "right margin, H:", "left margin, Hartlib:","bottom of page:"
                           ]

removed_what_follows_ang = ["H alters from", "H alters", "altered from ", "altered from", "? altered from", "H. alters",
                 "H alters from ?", "overwritten:", "overwritten in another hand?:", "overwritten in another hand:"]

annotations_sq = [
    # checked:
    "symbol",
    "blot", "MS hole", "MS torn",
    "abbrev.", "? abbrev.?",
    "altered", "Altered", "? Altered", "? altered", "altered?",
    "MS edge",  "MS torn", "? MS torn", "? MS edge", "? hole in MS",
    "left and right margins, Hartlib:", "left margin:", "left column:", "right column:", "right margin:", "right margin, H:", "left margin, H", "left margin, Hartlib:","bottom of page:",
    # not checked:
    "H capitalises",  "H. capitalises", "H capitalizes", "Hartlib:","H underlines", "H? alters",
    "top of page, another hand:", "another hand:", "another hand?:", "above address, another hand:", "scribal hand:", "Dury's hand:", "hand Y:",  "right margin, another hand:",  "first hand:", "Hand I:",  "bottom right, hand Z:",
    "upside down, Hartlib:", "Hartlib's hand:",
    "scribe:",
    "Dury:",
    "H deletes", "H punctuates","H deletes word",
    "seal", "Seal: snail", "seals", 'broken seal', "Seal",
    "squiggle", "squiggle?", "squiggles",
     "umlaut on v", "[q<i>uod?", "sic", "space", "capitalised", "gap", "decorative panel",
    "etc?", "deletion?",
    "?", "gap in MS",
    "mark", "post mark?",
    'blot/deletion', '? blot/deletion',
    'diagram: two grids with numbering at the top and dots within squares',
    '? faintly written below diagram', "dotted",
    # added:
    "? Blot", "? blotted"
]  # CHECK!!!!


annotations_ang = [
    # checked:
    "symbol",
    "blot", "MS hole", "MS torn",
    "abbrev.", "? abbrev.?",
    "altered", "Altered", "? Altered", "? altered", "altered?",
    "MS edge",  "MS torn", "? MS torn", "? MS edge", "? hole in MS",
    "left and right margins, Hartlib:", "left margin:", "left column:", "right column:", "right margin:", "right margin, H:", "left margin, Hartlib:", "left margin, H:", "bottom of page:",
    # not checked:
    "H capitalises",  "H. capitalises", "H capitalizes", "Hartlib:","H underlines", "H? alters",
    "top of page, another hand:", "another hand:", "another hand?:", "above address, another hand:", "scribal hand:", "Dury's hand:", "hand Y:",  "right margin, another hand:",  "first hand:", "Hand I:",  "bottom right, hand Z:",
    "upside down, Hartlib:", "Hartlib's hand:",
    "scribe:",
    "Dury:",
    "H deletes", "H punctuates","H deletes word",
    "seal", "Seal: snail", "seals", 'broken seal',
    "squiggle", "squiggle?", "squiggles",
     "umlaut on v", "[q<i>uod?", "sic", "space", "capitalised", "gap", "decorative panel",
    "etc?", "deletion?",
    "?", "gap in MS",
    "mark", "post mark?",
    'blot/deletion', '? blot/deletion',
    'diagram: two grids with numbering at the top and dots within squares',
    '? faintly written below diagram', "dotted",
    # added:
    "? Blot", "? blotted"
]  # CHECK!!!!

def clean_tags(text):
    # print("now...")
    # text = UnicodeDammit(text)
    try:
        text = UnicodeDammit.detwingle(text)
    except TypeError as e:
        print("dammint:" + str(e))
    # text = text.decode("utf8")
    print("Cleaning tags...")
    # if '\xa0' in text:
    #    print("found!!!!")
    # else:
    #    print("not found")
    # print("text:" + str(text))
    ##text = text.replace(u'\xa0', ' ')#.encode('utf-8')
    # if '\xa0' in text:
    #    print("found!!!!")
    # else:
    #    print("not found")
    # print("text without space:" + str(text))
    # print("unic:"+text.unicode_markup)
    # print("enco:"+text.original_encoding)

    # images are incorrectly tagged, because the closing tag </img> is missing; so I remove images and code of letter
    # at the top of each page myself:
    text = re.sub(r'onClick="(?:\\.|[^"\\])*"', '', text)
    images_pattern = re.compile(r'(<img[^>]*?>\[\d{1,3}\/(\d{1,3}\/)?\d{1,3}[A-Z]\])')
    # for image in re.findall(images_pattern, text.replace("'", "\\'")):
    for image in re.findall(images_pattern, text):
        text = text.replace(image[0], '')

    soup = BeautifulSoup(text, 'html.parser')
    # Remove all that is not the letter's text: header, images, notes, etc.:

    # Remove head tag:

    [s.extract() for s in soup('head')]

    # Remove body tag:
    for tag in soup.findAll('body'):
        tag.replaceWithChildren()


    # Remove hr tag:
    for tag in soup.findAll('hr'):
        tag.replaceWithChildren()

    # Remove p tag:
    for tag in soup.findAll('p'):
        tag.replaceWithChildren()

    # Remove image and code of letter at the top of each page, e.g. <hr><img  src="x.gif" align="right"   onClick="xyz('10_0062')">[10/2/28A]<br/><br/></p>:
    # NB: I've removed this code chunk because it's no longer necessary as I've already removed the image tags myself above
    # for tag in soup.find_all('img'):
    #    tag.replaceWith('')

    # Remove deleted content:
    # pseudo-code:
    # IF text MATCHES (<DEL>.*?</DEL>)
    # REMOVE \1
    for tag in soup.find_all('del'):
        tag.replaceWith('')

    # Ignore underline formatting:
    # Pseudo-code:
    # IF text MATCHES (<u>).*?(</u>)
    # REMOVE \1 AND \2
    for tag in soup.findAll('u'):
        tag.replaceWithChildren()

    # Ignore bold formatting:
    # Pseudo-code:
    # IF text MATCHES (<b>).*?(</b>)
    # REMOVE \1 AND \2
    for tag in soup.findAll('b'):
        tag.replaceWithChildren()

    # remove <sup> and <sub> tags:
    # Pseudo-code:
    # IF text MATCHES (<sub>)/(</sub>)
    # REMOVE \1 AND \2
    for tag in soup.findAll('sub'):
        tag.replaceWithChildren()

    for tag in soup.findAll('sup'):
        tag.replaceWithChildren()

    # remove annotations_sq like <TRANS SWITCH="2"> or <TRANS SWITCH="1">:
    for tag in soup.findAll("trans"):
        tag.replaceWithChildren()

    #all_tags = soup.find("html")
    #if all_tags is not None:
    #    # soup_final = "".join(str(item) for item in all_tags)
    #    soup_final = "".join(item.encode("utf-8") for item in all_tags)
    #else:
    #    soup_final = str(soup)
    soup_final = str(soup)

    # Remove <html tag:
    soup_final = re.sub(r'<(/)?html[^>]*?>', '', soup_final)
    # Remove <br/> tag:
    #soup_final = soup_final.replace("<br/>", "")
    soup_final = re.sub(r'<(/)?br(/)?>', '', soup_final, flags = re.I)
    # print("final:::")
    # if '\xa0' in text:
    #    print("found!!!!")
    # else:
    #    print("not found")
    return soup_final


def clean_text(text):
    # print("cleaning....")
    # if '\xa0' in text:
    #    print("found!!!!")
    # else:
    #    print("not found")

    # print("text0:"+text)
    text = text.replace('\xc2\xa0', ' ')
    #text = text.replace("\xa0", " ")
    # print("text1:"+text)
    # if '\xa0' in text:
    #    print("found!!!!")
    # else:
    #    print("not found")

    replacements = list()  # list of replacements for patterns

    # -----------------------------------
    # Square brackets:
    # -----------------------------------

    # find content between square brackets:

    sqbracket_patterns = []
    open_sqbrackets = []
    closed_sqbrackets = []
    matched_sqbrackets = 0
    index_open_sqbrackets = []
    index_closed_sqbrackets = []
    for i, c in enumerate(text):
        if c == '[':
            open_sqbrackets.append(i)
            matched_sqbrackets += 1
            index_open_sqbrackets.append(i)
        elif c == ']':
            closed_sqbrackets.append(i)
            matched_sqbrackets -= 1
            index_closed_sqbrackets.append(i)
        if matched_sqbrackets == 0 and index_open_sqbrackets and index_closed_sqbrackets:
            sqbracket_patterns.append((index_open_sqbrackets[0], index_closed_sqbrackets[-1]))
            index_open_sqbrackets = []
            index_closed_sqbrackets = []
    if len(open_sqbrackets) != len(closed_sqbrackets):
        print("Square brackets not matching!!")

    sqbracket_patterns = [text[ind1:ind2 + 1] for ind1, ind2 in sqbracket_patterns]

    # Ignore annotations_sq in italic text within square brackets:
    for sq_bracket_pattern in sqbracket_patterns:
        #sq_bracket_pattern = sq_bracket_pattern.replace("</i> <i>", "")
        new_sq_bracket_pattern = sq_bracket_pattern
        #threeitalic_sqbracket = re.match(u'\[(.*?)<i>(.*?)</i>(.*?)<i>(.*?)</i>(.*?)<i>(.*?)</i>(.*?)\]',
        #                                 new_sq_bracket_pattern)
        #twoitalic_sqbracket = re.match(u'\[(.*?)<i>(.*?)</i>(.*?)<i>(.*?)</i>(.*?)\]', new_sq_bracket_pattern)
        #oneitalic_sqbracket = re.match(u'\[(.*?)<i>(.*?)</i>(.*?)\]', new_sq_bracket_pattern)
        noitalic_sqbracket = re.match(u'\[([^<]+?)\]', new_sq_bracket_pattern)
        italic_texts = re.compile(r'<i>(.*?)</i>').findall(new_sq_bracket_pattern)
        roman_texts = re.compile(r'</i>(.*?)(?:<i>)?]$').findall(new_sq_bracket_pattern)
        print("------Squared bracket pattern before change:" + str(sq_bracket_pattern))
        if len(italic_texts) > 0:
            print("Italic text(s) in square brackets")
            replacements_italictexts = list()
            replacements_romantexts = list()
            for it in range(0,len(italic_texts)):
                italic_text = italic_texts[it]
                new_italic_text = ""
                new_roman_text = ""
                try:
                    roman_text = roman_texts[it]
                    roman_text = re.sub(r'<i>.*?</i>', '', roman_text)
                except:
                    roman_text = ""
                next_italic_text = ""
                if it+1 < len(italic_texts):
                    next_italic_text = italic_texts[it+1]
                previous_italic_text = ""
                if it-1 >= 0:
                    previous_italic_text = italic_texts[it-1]

                match_annotation = 0
                annotation_to_replace = ""

                for ann in annotations_sq:
                    if ann == italic_text and "altered" not in ann and ann not in ["?", "symbol"]:
                        match_annotation = match_annotation + 1
                        annotation_to_replace = ann
                    elif ann in italic_text and "altered" not in ann and ann not in ["?", "symbol"]: # cases like W: [Spee<i>de MS torn</i>]
                        match_annotation = match_annotation + 1
                        if len(ann) > len(annotation_to_replace):
                            annotation_to_replace = ann
                if previous_italic_text in removed_what_follows_sq:
                    new_italic_text = ""
                    new_roman_text = ""
                elif match_annotation > 0 and italic_text not in list_text_missing and \
                        (italic_text != "illeg" or roman_text != ".") and \
                        italic_text not in removed_what_follows_sq and "catchword:" not in italic_text:
                    print("0")
                    #new_sq_bracket_pattern = new_sq_bracket_pattern.replace(annotation_to_replace, "")
                    new_italic_text = italic_text.replace(annotation_to_replace, "")
                    new_roman_text = roman_text
                else:
                    if (italic_text in annotations_sq and italic_text != "?") or re.match(u'scribe [A-Z](\?)?:', italic_text) or \
                        re.match(u'hand [A-Z]\?:', italic_text) or re.match(u'p\. (\d)+?', italic_text) or \
                        re.match(u'(\d){1,2}[A-Z]{1,2}', italic_text):
                        #new_sq_bracket_pattern = new_sq_bracket_pattern.replace(italic_text, "")
                        new_italic_text = ""
                        new_roman_text = ""
                        print("1")
                    elif (italic_text == "hand" and next_italic_text != "" and re.match(r'[A-Z]:', next_italic_text)) or \
                            (previous_italic_text == "hand" and italic_text != "" and re.match(r'[A-Z]:', italic_text)):
                        #new_sq_bracket_pattern = ""
                        new_italic_text = ""
                        new_roman_text = ""
                        print("2")
                    elif italic_text == "H capitalis" and roman_text == "es":
                        #new_sq_bracket_pattern = ""
                        new_italic_text = ""
                        new_roman_text = ""
                        print("3")
                    elif italic_text in removed_what_follows_sq or "catchword:" in italic_text:
                        #new_sq_bracket_pattern = new_sq_bracket_pattern.replace(italic_text, "").replace(roman_text, "")
                        new_italic_text = ""
                        new_roman_text = ""
                        print("4")
                    elif italic_text in list_text_missing or (italic_text == "illeg" and roman_text == "."):
                        #new_sq_bracket_pattern = "TEXT_MISSING"
                        new_italic_text = "TEXT_MISSING"
                        new_roman_text = ""
                        print("5")
                    elif ((roman_text != "" and italic_text == "Greek:") or (italic_text == "word deleted" and roman_text == "")):
                        #new_sq_bracket_pattern = roman_text
                        new_italic_text = ""
                        new_roman_text = roman_text
                        print("6")
                    elif italic_text == "left margin:":
                        print("7")
                        if roman_text == " X":
                            #new_sq_bracket_pattern = ""
                            new_italic_text = ""
                            new_roman_text = ""
                        else:
                            #new_sq_bracket_pattern = roman_text
                            new_italic_text = ""
                            new_roman_text = roman_text
                    elif re.match(u'left margin(.*?)$', italic_text):
                        lm = re.match(u'left margin(.*?)$', italic_text)
                        #new_sq_bracket_pattern = lm.group(1)
                        new_italic_text = lm.group(1)
                        new_roman_text = ""
                        print("8")
                    elif re.match(u'scribe [A-Z](\?)?:', italic_text):
                        #new_sq_bracket_pattern = roman_text
                        new_italic_text = ""
                        new_roman_text = roman_text
                        print("9")
                    elif "Hebrew:" in italic_text:  # add other languages!
                        hebrew = re.match(u'Hebrew: (.*)', italic_text)
                        hebrew1 = hebrew.group(1)
                        #new_sq_bracket_pattern = hebrew1
                        new_italic_text = hebrew1
                        new_roman_text = ""
                        print("10")
                    elif italic_text in ["left margin:", "left margin: *", "H:", "Hartlib:", "H?:"]:
                        #new_sq_bracket_pattern = roman_text
                        new_italic_text = ""
                        new_roman_text = roman_text
                        print("10a")
                    elif "symbol: " in italic_text:
                        print("11")
                        symb = re.match(u'^symbol: (.+?)$', italic_text)
                        symb1 = symb.group(1)
                        #new_sq_bracket_pattern = new_sq_bracket_pattern.replace(italic_text, symb1)
                        new_italic_text = symb1
                        new_roman_text = ""
                    elif "?" in italic_text:
                        #new_sq_bracket_pattern = new_sq_bracket_pattern.replace("?", "")
                        new_italic_text = italic_text.replace("?", "")
                        new_roman_text = ""
                    else:
                        print("12")
                        mstorn = re.match(u'^(.+?)(\?)? MS (torn|edge)', italic_text)  # as in the test "W: [Speede MS torn]"
                        if mstorn:
                            before_mstorn = mstorn.group(1)
                            if before_mstorn in list_text_missing:
                                #new_sq_bracket_pattern = "TEXT_MISSING"
                                new_italic_text = "TEXT_MISSING"
                                new_roman_text = ""
                            else:
                                #new_sq_bracket_pattern = new_sq_bracket_pattern
                                new_italic_text = italic_text
                                new_roman_text = ""
                        elif "?" in italic_text:  # case [q<i>uod?</i>]
                            #new_sq_bracket_pattern = new_sq_bracket_pattern.replace("?", "").replace("[", "").replace("]", "")
                            new_italic_text = italic_text.replace("?", "").replace("[", "").replace("]", "")
                            new_roman_text = ""
                        else:
                            #new_sq_bracket_pattern = new_sq_bracket_pattern.replace("[", "").replace("]", "")
                            new_italic_text = italic_text.replace("[", "").replace("]", "")
                            new_roman_text = roman_text

                if roman_text == " ":
                    new_roman_text = " "
                replacements_italictexts.append((italic_text, new_italic_text))
                replacements_romantexts.append((roman_text, new_roman_text))

            for i in range(0,len(replacements_italictexts)):
                remove_it = replacements_italictexts[i][0]
                include_it = replacements_italictexts[i][1]
                print("remove it:" + remove_it)
                print("include it:" + include_it)
                print("replacements....")
                print("text:" + new_sq_bracket_pattern)
                if remove_it in new_sq_bracket_pattern:
                    print("remove it in text!!!")
                    new_sq_bracket_pattern = new_sq_bracket_pattern.replace(remove_it, include_it)  # .strip())
                else:
                    print("remove not in text!!!")
                print("prefinal:" + str(new_sq_bracket_pattern))

            for i in range(0,len(replacements_romantexts)):
                remove_rom = replacements_romantexts[i][0]
                include_rom = replacements_romantexts[i][1]
                print("remove rom:" + remove_rom)
                print("include rom:" + include_rom)
                print("replacements....")
                if remove_rom in new_sq_bracket_pattern:
                    print("remove rom in text!!!")
                    new_sq_bracket_pattern = new_sq_bracket_pattern.replace(remove_rom, include_rom)  # .strip())
                else:
                    print("remove not in text!!!")
                print("prefinal:" + str(new_sq_bracket_pattern))

            new_sq_bracket_pattern = new_sq_bracket_pattern.replace("<i>", "").replace("</i>", "").replace("[", "").replace("]", "")
            try:
                new_sq_bracket_pattern = new_sq_bracket_pattern.replace("  ", " ")
            except:
                print("no double space in new_sq_bracket_pattern")

        else:
            print("No italic text between square brackets")
            print("noitalic_sqbracket:"+str(noitalic_sqbracket))
            text_sqbr = ""
            if noitalic_sqbracket:
                text_sqbr = noitalic_sqbracket.group(1)
            print("text_sqbr:" + text_sqbr)
            # remove annotations_sq:
            if text_sqbr in ['seal', 'line deleted', 'letter deleted?', '?', 'bottom of page, upside down:',
                             'squiggle', 'letter finished in German', 'left margin:',
                             'H? crosses through preceding two lines', 'symbol?', "overwritten in another hand:",
                             "Greek word deleted", "one word deleted"] or "catchword:" in text_sqbr:
                new_sq_bracket_pattern = ""
                print("a")
            elif re.match(u'p\. (\d)+?', text_sqbr):
                new_sq_bracket_pattern = ""
                print("b")
            elif text_sqbr in list_text_missing:
                new_sq_bracket_pattern = "TEXT_MISSING"
                print("c")
            elif re.match(u'(.+?)\?', text_sqbr):
                qu = re.match(u'(.+?)\?', text_sqbr)
                new_sq_bracket_pattern = qu.group(1)
                print("d")
            elif "left margin" in text_sqbr:
                new_sq_bracket_pattern = new_sq_bracket_pattern.replace(text_sqbr, "")
            elif re.match(u'^=(.+?)$', text_sqbr) and not re.match(u'^=(.+?)\?$', text_sqbr):
                new_sq_bracket_pattern = "!!!" + re.match(u'^=(.+?)$', text_sqbr).group(1)
            elif noitalic_sqbracket:
                new_sq_bracket_pattern = noitalic_sqbracket.group(0)
            else:
                new_sq_bracket_pattern = ""

        print("------After sq:" + str(new_sq_bracket_pattern))

        replacements.append((sq_bracket_pattern, new_sq_bracket_pattern))

    # sort the replacements
    replacements = sorted(replacements, key=lambda x: len(x[0]), reverse=True)

    for remove, include in replacements:
        print("remove:" + remove)
        print("include:" + include)
        print("replacements....")
        print("text:" + text)
        if remove in text:
            print("remove in text!!!")
            text = text.replace(remove, include)  # .strip())
        else:
            print("remove not in text!!!")
        print("prefinal:" + str(text))

    # find content between angular brackets:

    angbracket_patterns_w = []
    angbracket_patterns_c = []
    index_open_angbrackets_w = []  # contains the index of the word containing the open angular bracket sign
    index_open_angbrackets_c = []  # contains the index of the first character in the word containing the open angular bracket sign
    open_angbrackets = []  # contains the index of the word containing the open angular bracket sign
    index_closed_angbrackets_w = []  # contains the index of the first character in the word containing the closed angular bracket sign
    index_closed_angbrackets_c = []  # contains the index of the first character in the word containing the closed angular bracket sign
    closed_angbrackets = []
    matched_angbrackets = 0
    text = text.replace("&lt;", " &lt; ")
    text = text.replace("&gt;", " &gt; ")
    text = text.replace("  ", " ")
    print("text:" + text)
    words = text.split()
    for i in range(0, len(words)):
        word = words[i]
        left = re.match('.*?&lt;.*?', word)
        right = re.match('.*?&gt;.*?', word)
        if left:
            j = word.index('&lt;')
            index_open_angbrackets_w.append(i)
            index_open_angbrackets_c.append(j)
            matched_angbrackets += 1
        if right:
            j = word.index('&gt;')
            index_closed_angbrackets_w.append(i)
            index_closed_angbrackets_c.append(j)
            matched_angbrackets -= 1
        if matched_angbrackets == 0 and index_open_angbrackets_w and index_open_angbrackets_c and \
                index_closed_angbrackets_w and index_closed_angbrackets_c:
            angbracket_patterns_w.append((index_open_angbrackets_w[0], index_closed_angbrackets_w[-1]))
            angbracket_patterns_c.append((index_open_angbrackets_c[0], index_closed_angbrackets_c[-1]))
            index_open_angbrackets_w = []
            index_open_angbrackets_c = []
            index_closed_angbrackets_w = []
            index_closed_angbrackets_c = []
    if len(open_angbrackets) != len(closed_angbrackets):
        print("Angular brackets not matching!!")

    if angbracket_patterns_w:
        # print(str(angbracket_patterns_w))
        angbracket_patterns = [" ".join(words[ind1:ind2 + 1]) for ind1, ind2 in angbracket_patterns_w]

        # Ignore annotations_ang in italic text within angular brackets:
        for ang_bracket_pattern in angbracket_patterns:
            new_ang_bracket_pattern = ang_bracket_pattern
            #twoitalic_angbracket = re.match(u'&lt;(.*?)<i>(.*?)</i>(.*?)<i>(.*?)</i>(.*?)&gt;', new_ang_bracket_pattern)
            #oneitalic_angbracket = re.match(u'&lt;(.*?)<i>(.*?)</i>(.*?)&gt;', new_ang_bracket_pattern)
            noitalic_angbracket = re.match(u'&lt;([^<]+?)&gt;', new_ang_bracket_pattern)
            italic_texts = re.compile(r'<i>(.*?)</i>').findall(new_ang_bracket_pattern)
            roman_texts = re.compile(r'</i>(.*?)(?:<i>)?&gt;$').findall(new_ang_bracket_pattern)
            print("---Angular bracket pattern before:" + str(ang_bracket_pattern))

            if len(italic_texts) > 0:
                print("Italic text(s) in square brackets")
                replacements_italictexts = list()
                replacements_romantexts = list()
                for it in range(0,len(italic_texts)):
                    italic_text = italic_texts[it]
                    new_italic_text = ""
                    new_roman_text = ""
                    try:
                        roman_text = roman_texts[it]
                    except:
                        roman_text = ""
                    next_italic_text = ""
                    if it+1 < len(italic_texts):
                        next_italic_text = italic_texts[it+1]
                    previous_italic_text = ""
                    if it-1 >= 0:
                        previous_italic_text = italic_texts[it-1]
                    match_annotation = 0
                    annotation_to_replace = ""

                    for ann in annotations_ang:
                        if ann == italic_text and "altered" not in ann and ann not in ["?", "symbol"]:
                            match_annotation = match_annotation + 1
                            annotation_to_replace = ann
                        elif ann in italic_text and "altered" not in ann and ann not in ["?", "symbol"]: # cases like W: [Spee<i>de MS torn</i>]
                            match_annotation = match_annotation + 1
                            if len(ann) > len(annotation_to_replace):
                                annotation_to_replace = ann
                        else:
                            match_annotation = match_annotation
                    if previous_italic_text in removed_what_follows_ang:
                        new_italic_text = ""
                        new_roman_text = ""
                    elif match_annotation > 0 and italic_text not in list_text_missing and \
                            (italic_text != "illeg" or roman_text != ".") and \
                            italic_text not in removed_what_follows_ang and "catchword:" not in italic_text and\
                            italic_text != "left margin, another hand:" and (italic_text != "H" or not roman_text.startswith(":")):
                        print("0")
                        new_italic_text = italic_text.replace(annotation_to_replace, "")
                        new_roman_text = roman_text
                    else:
                        if (((italic_text == "left" and next_italic_text == "margin:") or (italic_text == "margin:" and previous_italic_text == "left")) or \
                                    ((previous_italic_text == "left" and italic_text == "margin:") or (previous_italic_text == "margin:" and italic_text == "left"))):
                            new_italic_text = ""
                            new_roman_text = ""

                        #elif italic_text in ["left margin:", "Hartlib:"]:
                        #    print("-2")
                        #    new_italic_text = ""
                        #    new_roman_text = roman_text
                        elif italic_text == "left margin, another hand:":
                            print("-1")
                            new_italic_text = ""
                            new_roman_text = roman_text
                        elif italic_text == "H" and roman_text.startswith(":"):
                            print("0")
                            new_italic_text = ""
                            new_roman_text = roman_text[1:]
                            #roman_text = roman_text[1:]
                        elif italic_text in annotations_ang or re.match(u'scribe [A-Z](\?)?:', italic_text) or re.match(u'hand [A-Z]\?:', italic_text) or re.match(u'p\. (\d)+?', italic_text) or re.match(u'(\d){1,2}[A-Z]{1,2}', italic_text):
                            new_italic_text = ""
                            new_roman_text = ""
                            print("1")
                        elif (italic_text == "hand" and next_italic_text != "" and re.match(r'[A-Z]:', next_italic_text)) or \
                                (previous_italic_text == "hand" and italic_text != "" and re.match(r'[A-Z]:', italic_text)):
                            new_italic_text = ""
                            new_roman_text = ""
                            print("2")
                        elif italic_text == "H capitalis" and roman_text == "es":
                            new_italic_text = ""
                            new_roman_text = ""
                            print("3")
                        elif italic_text in removed_what_follows_ang or "catchword:" in italic_text:
                            new_italic_text = ""
                            new_roman_text = ""
                            print("4")
                        elif italic_text in list_text_missing or (italic_text == "illeg" and roman_text == "."):
                            new_italic_text = "TEXT_MISSING"
                            new_roman_text = ""
                            print("5")
                        elif ((roman_text != "" and italic_text == "Greek:") or (italic_text == "word deleted" and roman_text == "")):
                            new_italic_text = ""
                            new_roman_text = roman_text
                            print("6")
                        elif italic_text == "left margin:":
                            print("7")
                            if roman_text == " X":
                                new_italic_text = ""
                                new_roman_text = ""
                            else:
                                new_italic_text = ""
                                new_roman_text = roman_text
                        elif re.match(u'left margin(.*?)$', italic_text):
                            lm = re.match(u'left margin(.*?)$', italic_text)
                            new_italic_text = lm.group(1)
                            new_roman_text = ""
                            print("8")
                        elif re.match(u'scribe [A-Z](\?)?:', italic_text):
                            new_italic_text = ""
                            new_roman_text = roman_text
                            print("9")
                        elif "Hebrew:" in italic_text:  # add other languages!
                            hebrew = re.match(u'Hebrew: (.*)', italic_text)
                            hebrew1 = hebrew.group(1)
                            new_italic_text = hebrew1
                            new_roman_text = ""
                            print("10")
                        elif italic_text in ["H:", "Hartlib:", "H?:"] or italic_text == "Hartlib" and roman_text == ":":
                            print("10a")
                            new_italic_text = ""
                            new_roman_text = roman_text
                        elif "symbol: " in italic_text:
                            print("11")
                            symb = re.match(u'^symbol: (.+?)$', italic_text)
                            symb1 = symb.group(1)
                            new_italic_text = symb1
                            new_roman_text = ""
                        elif "?" in italic_text:
                            new_italic_text = italic_text.replace("?", "")
                            new_roman_text = ""
                        else:
                            print("12")
                            mstorn = re.match(u'^(.+?)(\?)? MS (torn|edge)', italic_text)  # as in the test "W: [Speede MS torn]"
                            if mstorn:
                                print("a")
                                before_mstorn = mstorn.group(1)
                                if before_mstorn in list_text_missing:
                                    new_italic_text = "TEXT_MISSING"
                                    new_roman_text = ""
                                else:
                                    new_italic_text = italic_text
                                    new_roman_text = ""
                            elif "?" in italic_text:  # case [q<i>uod?</i>]
                                print("b")
                                new_italic_text = italic_text.replace("?", "").replace("[", "").replace("]", "")
                                new_roman_text = ""
                            else:
                                print("c")
                                new_italic_text = italic_text.replace("&lt;", "").replace("&gt;", "")
                                new_roman_text = roman_text

                    replacements_italictexts.append((italic_text, new_italic_text))
                    replacements_romantexts.append((roman_text, new_roman_text))

                for i in range(0,len(replacements_italictexts)):
                    remove_it = replacements_italictexts[i][0]
                    include_it = replacements_italictexts[i][1]
                    print("remove it:" + remove_it)
                    print("include it:" + include_it)
                    print("replacements....")
                    print("text:" + new_ang_bracket_pattern)
                    if remove_it in new_ang_bracket_pattern:
                        print("remove it in text!!!")
                        new_ang_bracket_pattern = new_ang_bracket_pattern.replace(remove_it, include_it)  # .strip())
                    else:
                        print("remove not in text!!!")
                    print("prefinal:" + str(new_ang_bracket_pattern))

                for i in range(0,len(replacements_romantexts)):
                    remove_rom = replacements_romantexts[i][0]
                    include_rom = replacements_romantexts[i][1]
                    print("remove rom:" + remove_rom)
                    print("include rom:" + include_rom)
                    print("replacements....")
                    if remove_rom in new_ang_bracket_pattern:
                        print("remove rom in text!!!")
                        new_ang_bracket_pattern = new_ang_bracket_pattern.replace(remove_rom, include_rom)  # .strip())
                    else:
                        print("remove not in text!!!")
                    print("prefinal:" + str(new_ang_bracket_pattern))

                new_ang_bracket_pattern = new_ang_bracket_pattern.replace("<i>", "").replace("</i>", "").replace("&lt;", "").replace("&gt;", "")
                try:
                    new_ang_bracket_pattern = new_ang_bracket_pattern.replace("  ", " ")
                except:
                    print("no double space in new_ang_bracket_pattern")

            else:
                print("No italic text between angular brackets")
                text_sqbr = ""
                if noitalic_angbracket:
                    text_sqbr = noitalic_angbracket.group(1)
                print("text_sqbr:" + text_sqbr)
                # remove annotations_sq:
                if text_sqbr in ['seal', 'line deleted', 'letter deleted?', '?', 'bottom of page, upside down:',
                                 'squiggle', 'letter finished in German', 'left margin:',
                                 'H? crosses through preceding two lines', 'symbol?', "overwritten in another hand:",
                                 "Greek word deleted", "one word deleted"] or "catchword:" in text_sqbr:
                    new_ang_bracket_pattern = ""
                    print("a")
                elif re.match(u'p\. (\d)+?', text_sqbr):
                    new_ang_bracket_pattern = ""
                    print("b")
                elif text_sqbr in list_text_missing:
                    new_ang_bracket_pattern = "TEXT_MISSING"
                    print("c")
                elif re.match(u'(.+?)\?', text_sqbr):
                    qu = re.match(u'(.+?)\?', text_sqbr)
                    new_ang_bracket_pattern = qu.group(1)
                    print("d")
                elif "left margin" in text_sqbr:
                    new_ang_bracket_pattern = new_ang_bracket_pattern.replace(text_sqbr, "")
                elif re.match(u'^=(.+?)$', text_sqbr) and not re.match(u'^=(.+?)\?$', text_sqbr):
                    new_ang_bracket_pattern = "!!!" + re.match(u'^=(.+?)$', text_sqbr).group(1)
                elif noitalic_angbracket:
                    new_ang_bracket_pattern = noitalic_angbracket.group(0)
                else:
                    new_ang_bracket_pattern = ""

            print("------After sq:" + str(new_ang_bracket_pattern))

            replacements.append((ang_bracket_pattern, new_ang_bracket_pattern))

    # sort the replacements
    replacements = sorted(replacements, key=lambda x: len(x[0]), reverse=True)

    for remove, include in replacements:
        print("remove:" + remove)
        print("include:" + include)
        print("replacements....")
        print("text:" + text)
        if remove in text:
            print("remove in text!!!")
            text = text.replace(remove, include)  # .strip())
        elif remove in text.replace("  ", " ").rstrip().lstrip().replace("  ", " "):
            print("remove in text!!!")
            text = text.replace("  ", " ").rstrip().lstrip().replace("  ", " ")
            text = text.replace(remove, include)  # .strip())
        else:
            print("remove not in text!!!")
        print("prefinal:" + str(text))

    # Remove italic formatting left (outside brackets):
    if "<i>" in text:
        text = text.replace("<i>", "").replace("</i>", "")

    text = text.replace("&lt;", "").replace("&gt;", "")
    # Remove HTML tag:

    # soup = BeautifulSoup(text, 'html.parser')
    # for tag in soup.findAll('html'):
    #    tag.replaceWithChildren()

    if "<html>" in text:
        text = text.replace("<html>", "").replace("</html>", "")

    # in cases like audio[=audeo] we only want audeo:
    print("ecco")
    eqs = re.compile(r"^(.*?)\b([^ ]+?)\!\!\!([^ ]+?)\b(.*?)$").findall(text)
    for eq in eqs:
        print("1!!!!")
        text = eq[0] + " " + eq[2] + " " + eq[3]
    eqs = re.compile(r"^(.+?)\b([^ ]+?)\=([^ ]+?)\b(.+?)$").findall(text)
    for eq in eqs:
        print("2!!!!")
        text = eq[0] + " " + eq[2] + " " + eq[3]
    text = text.replace("\xc2", "")
    text = text.replace("amp;", "")
    text = text.replace("#", "")
    text = text.replace("*", "")
    text = text.replace("  ", " ").rstrip().lstrip()
    text = text.replace("  ", " ").replace("()", "").replace(" , ", ", ").replace(" ;", ";").replace("  ", " ")
    text = re.sub(r'  ', ' ', text)
    text = text.replace("  ", " ").rstrip().lstrip()

    print("final:" + str(text))
    return text


# --------------------------
# Testing
# --------------------------

count_successful_tests = 0

# with codecs.open(os.path.join(dir_tests, test_output_file_summary), 'w', "utf-8") as summary_testing:
with open(os.path.join(dir_tests, test_output_file_summary), 'w') as summary_testing:
    writer_summary = csv.writer(summary_testing, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL,
                                lineterminator='\n')
    writer_summary.writerow(['date', 'time', 'number of test input', 'number of successful tests',
                             'proportion of successful tests'])

    with open(os.path.join(dir_tests, test_output_file), 'w') as testing_output:
        # with codecs.open(os.path.join(dir_tests, test_output_file), 'w', "utf-8") as testing_output:
        writer = csv.writer(testing_output, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL,
                            lineterminator='\n')
        writer.writerow(['input', 'correct_output', 'actual_output', 'same'])

        count_tests = 1
        for t in unit_tests_input:
            count_tests += 1
            if num_test != "" and count_tests == int(num_test) or num_test == "" and count_tests > 0:
                print("Test number " + str(count_tests))
                print("---before:" + str(t))
                correct_output = unit_tests[t]  # .encode("utf-8")
                actual_output0 = clean_tags(t)
                print("----after cleaning tags:" + str(actual_output0))
                actual_output = clean_text(actual_output0)  # .encode("utf-8")
                print("---after cleaning text:" + str(actual_output))

                same = "no"
                if correct_output == actual_output:
                    same = "yes"
                    count_successful_tests += 1
                    print("same!!!!")
                try:
                    writer.writerow([t, correct_output, actual_output, same])
                except:
                    print("Error!!!!!!!!!!!")

                num_tests = len(unit_tests.keys())
                prop_successful_tests = count_successful_tests / num_tests

    writer_summary.writerow(
        [time.strftime("%x"), time.strftime("%X"), str(num_tests), str(count_successful_tests),
         "%.2f" % prop_successful_tests])
    print(str(count_successful_tests) + " successful tests out of " + str(num_tests))
    print("proportion of successful tests: %.2f" % prop_successful_tests)

# --------------------------
# Process letters
# --------------------------

files = [f for f in listdir(dir_in) if isfile(join(dir_in, f)) and f.startswith("1")]
if istest == "yes":
    #files = ["ADD4279_41.html"]
    #files = ["test.html"]
    files = []

for file in files:
    print("file:" + file)
    html = codecs.open(os.path.join(dir_in, file), 'r').read()#.replace('\n', ' ').replace("  ", " ")\
        #.replace('\r', ' ').replace("  ", " ").replace("  ", " ")
    # remove new lines from file text:

    cleaned_text0 = clean_tags(html)
    cleaned_text = clean_text(cleaned_text0)
    cleaned_text = cleaned_text.replace("  ", " ")

    file_out = file.replace(".html", "_cleaned.txt")
    # output = codecs.open(os.path.join(dir_out, file_out), "w", "utf-8")
    output = open(os.path.join(dir_out, file_out), "w")
    output.write(cleaned_text)
    output.close()
