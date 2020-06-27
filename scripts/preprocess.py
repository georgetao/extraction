#!/usr/bin/python

# imports
import re
import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize  

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
WB = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""
BLACK = "[^A-Za-z0-9\s\?!,'\.;:/\-@*%#~&]+"


# Strings
BREAK = 'BREAK'
FORWARD = 'Forwarded by'
SPACE = ' '
EMAIL = 'EMAILADDRESS'
PHONE = 'PHONENUMBER'
WEB = 'WEBSITE'

# Personal information strings
INFO_CATS = {EMAIL, PHONE, WEB}

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
    text = re.sub(break_regex, BREAK, text)
    text = re.sub(HTML, SPACE, text)
    text = re.sub(PH, phone_repl, text)
    text = re.sub(BLACK, SPACE, text)
    text = re.sub(WHITE, SPACE, text)
    text = text.strip()
    return text


def clean_info(text):
    text = re.sub(EA, SPACE+EMAIL+SPACE, text)
    text = re.sub(PH, SPACE+PHONE+SPACE, text)
    text = re.sub(WB, SPACE+ WEB +SPACE, text)
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


def format_phone_number(phone_number):
    """Formatting a phone number according to NANP Style
    """
    # remove non digits
    digs = re.sub(NON_NUM, '', phone_number)
    # break into area and local
    area, loc3, loc4 = digs[:-7], digs[-7:-3], digs[-3:]
    
    if len(area) == 0:
        return f' {loc3}-{loc4} '
    elif len(area) <= 3:
        return f' {area}-{loc3}-{loc4} '
    else:
        country, area = area[:-3], area[-3:]
        return f' {country}-{area}-{loc3}-{loc4} '



###### Processing for Examples #######

import en_core_web_sm
nlp = en_core_web_sm.load()

ENT_TAGS = {
    'PERSON',
    'NORP',
    'FAC',
    'ORG',
    'GPE',
    'LOC',
    'PRODUCT',
    'EVENT'
    'WORK_OF_ART',
    'LAW',
    'LANGUAGE',
    'DATE',
    'TIME',
    'PERCENT',
    'MONEY',
    'QUANTITY',
    'ORDINAL',
    'CARDINAL'
}

CAP_WORDS = {'SENDER', 'I'}.union(INFO_CATS, ENT_TAGS)


def process_text(text):
    text = clean_info(text)
    text = replace_NE(text)
    text = re.sub(BLACK, '', text)
    tokens = [t if t in CAP_WORDS else t.lower() for 
              t in word_tokenize(text)]
    return tokens


def replace_NE(text):
    'Replace the named entities with their types'
    ent_lab = {e.text: e.label_ for e in nlp(text).ents if 
               e.text not in INFO_CATS}
    for ent, lab in ent_lab.items():
        text = re.sub(ent, lab, text)
    return text

