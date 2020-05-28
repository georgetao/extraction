#!/usr/bin/python

# imports
import sys
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
    # text = re.sub(BLACK, SPACE, text)
    text = text.strip()
    return text

for line in sys.stdin:
   
    try:
        # load
        message, task = line.split('\t')
        # clean
        task, message = clean(task), clean(message)    
        sents = sum([sent_tokenize(m) for m in message.split(BREAK)], [])

        # identify entire task sentence
        i = np.argmax([bool(re.search(task, s)) for s in sents])
        ts = sents[i]

        # identify context
        if i > 0 and not re.search(comp_regex, sents[i-1]):
            cs = sents[i-1]
            context_sents = [s for s in sents[:i-1] if not re.search(comp_regex, s)]
            context = '. '.join(context_sents)
        else:
            cs, context = '',''

        # print
        print(f'{task}\t{clean_info(context)}\t{clean_info(cs)}\t{clean_info(ts)}')
        
    except:
        continue
