#!/usr/bin/python

# imports
import re
import numpy as np
from nltk.tokenize import sent_tokenize

# Regexes
HTML = r'</?\w+/?>|>|<'
BR = r'</?br/?>'
BRBR = BR+BR
MARK = r'</?mark/?>|>|<'
WHITE = r'\s+'
HYPHENS = r'---+'
YW = "you wrote:"

EMAIL_TIME = "[0-9]?[0-9]:[0-9][0-9]\s[AP]M"
EA = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
PH = r"(\d{0,2}[\s\.-]{0,3}\(?\d{0,3}\)?[\s\.-]{0,3}\d{3}[\s\.-]{0,3}\d{4})"
BLACK = "[^A-Za-z0-9\s\?!,\.;:/-]+"


# Strings
BREAK = 'BREAK'
FORWARD = 'Forwarded by'
SPACE = ' '
EMAIL = ' EMAILADDRESS '
PHONE = ' PHONE '

# components
email_components = [
    'Date:',
    'From:',
    'To:',
    'Subject:',
    'Re:',
    'Mime-Version:',
    'Content-Type:',
    'Content-Transfer-Encoding:',
    '-From:',
    '-To:',
    '-cc:',
    '-bcc:',
    '-Folder:',
    '-Origin:',
    '-FileName:'
]

##### Preprocessing Functions ####

def make_regex(lst):
    return '|'.join(lst)

break_regex = make_regex([BRBR, HYPHENS, YW])
comp_regex = make_regex(email_components+[EMAIL_TIME])

def clean(text):
    text = re.sub(break_regex, BREAK, text)
    text = re.sub(HTML, SPACE, text)
    text = re.sub(BLACK, SPACE, text)
    text = text.strip()
    return text

def clean_info(text):
    text = re.sub(EA, EMAIL, text)
    text = re.sub(PH, PHONE, text)
    text = re.sub(WHITE, SPACE, text)
    text = text.strip()
    return text
        
    
def trim_sents(sents, max_tokens=75):
    """Take the most sentences from the tail that together meet the tokens requirement
    """
    lens = [len(s.split()) for s in sents]
    trimmed_sents = [sents[i] for i in range(len(lens)) 
                 if sum(lens[i:]) <= max_tokens]
    return trimmed_sents
