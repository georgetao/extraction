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
NON_NUM = '[^0-9]'

EMAIL_TIME = "[0-9]?[0-9]:[0-9][0-9]\s[AP]M"
EA = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
PH = r"(\d{0,2}[\s\.-]{0,3}\(?\d{0,3}\)?[\s\.-]{0,3}\d{3}[\s\.-]{0,3}\d{4})"
BLACK = "[^A-Za-z0-9\s\?!,'\.;:/\-@*%#~&]+"


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

def phone_repl(matchobj):
    return format_phone_number(matchobj.group())

break_regex = make_regex([BRBR, HYPHENS, YW])
comp_regex = make_regex(email_components+[EMAIL_TIME])

def clean(text):
    text = re.sub(break_regex, BREAK, str(text))
    text = re.sub(HTML, SPACE, str(text))
    text = re.sub(PH, phone_repl, str(text))
    text = re.sub(BLACK, SPACE, str(text))
    text = re.sub(WHITE, SPACE, str(text))
    text = text.strip()
    return text


def clean_info(text):
    text = re.sub(EA, EMAIL, str(text))
    text = re.sub(PH, PHONE, str(text))
    text = re.sub(WHITE, SPACE, str(text))
    text = text.strip()
    return text
        
    
def trim_sents(sents, max_tokens=75):
    """Take the most sentences from the tail that together meet the tokens requirement
    """
    lens = [len(s.split()) for s in sents]
    trimmed_sents = [sents[i] for i in range(len(lens)) 
                     if sum(lens[i:]) <= max_tokens]
    return trimmed_sents


def format_phone_number(phone_number):
    """Formatting a phone number according to NANP Style
    """
    # remove non digits
    digs = re.sub(NON_NUM, '', phone_number)
    # break into area and local
    area, loc3, loc4 = digs[:-7], digs[-7:-4], digs[-4:]
    
    if len(area) == 0:
        return f' {loc3}-{loc4} '
    elif len(area) <= 3:
        return f' {area}-{loc3}-{loc4} '
    else:
        country, area = area[:-3], area[-3:]
        return f' {country}-{area}-{loc3}-{loc4} '
