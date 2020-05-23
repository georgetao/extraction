#!/usr/bin/python

# imports
import sys
import re
import numpy as np
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize

# Regexes
HTML = r'</?\w+/?>|>|<'
WHITE = r'\s+'
FORWARD = 'Forwarded by'
SPACE = ' '

# helper functions
# erase_html = lambda r: BeautifulSoup(r, 'html5lib').get_text().strip()

def erase_html(text):
    text = re.sub(HTML, SPACE, text)
    text = re.sub(WHITE, SPACE, text)
    text = text.strip()
    return text

# def clean(raw):
#     # tokenize into sentences
#     sentences = sent_tokenize(erase_html(raw))
#     return sentences

for line in sys.stdin:
    # load
    message, task = line.split('\t')
    
    # clean
    task, message = erase_html(task), erase_html(message)
    sents = sent_tokenize(message)
    
    # identify task sentence
    is_task = [bool(re.search(task, s)) for s in sents]
    i = np.argmax([bool(re.search(task, s)) for s in sents])
    print(is_task)
    ts = sents[i]
    if i > 0:
        cs = sents[i-1]
    else:
        cs = ''
    
    # print(f'{cs}\t{ts}')
    print(50*'=')
    print('TASK', task)
    print('CCCC', cs)
    print('TSTS', ts)
    print('####', message)

    
   
