#!/usr/bin/python

# imports
import re
import numpy as np
# from nltk.tokenize import sent_tokenize, word_tokenize

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
PH = r"(\d{0,2}[\s\.-]{0,3}\(?\d{0,3}\)?[\s\.-]{0,3}\d{3,4}[\s\.-]{0,3}\d{3,4})\b"
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


######################################
###### Processing for Examples #######
######################################

# imports
import spacy
from collections import OrderedDict

# Regexes
BAD_20 = r'\b20\b'
ANYSPACE = '[\t\n\s]'
SENDER = 'SENDER'
ENRON = r'\b(Enron|enron|ENRON)\b'
EMAIL_WORD = r'\b[Ee]\s?-?\s?[Mm][Aa][Ii][Ll]\b'
ERASE = BAD_20 + '|' + BLACK
BLACK_NO_PER = "[^A-Za-z0-9\s\?!,';:/\-@*%#~&]+"
EXT_PER = r'[\.\?\!,]\.' # extra period
ext_per_repl = lambda match: match.group()[0]   # extra period fixer

# Constants
CAP_WORDS = {'I'}

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

expressions = {
    PHONE:  PH,
    EMAIL:  EA,
    WEB:    WB,
    SENDER: SENDER,
    'ORG':  ENRON
}

ENT_TAGS = ENT_TAGS.union(expressions.keys())


# Helper Functions
def ranges_overlap(a1, a2, b1, b2):
    'Assume a1 < a2 and b1 < b2'
    return not(max(a1, a2) < min(b1, b2) or max(b1, b2) < min(a1, a2))

def compatible_with_ranges(start, end, ranges):
    return not any([ranges_overlap(start, end, s, e) for s,e in ranges])

def tighten_bounds(start, end, text):
    'Tighten the bounds around a match'
    while re.match(ANYSPACE, text[start]): start += 1
    while re.match(ANYSPACE, text[end-1]): end -= 1
    return start, end

def lower_first_token(text):
    split = text.split(' ', 1)
    if len(split) == 2:
        return split[0].lower() + ' ' + split[1]
    else:
        assert len(split) == 1
        return split[0].lower()

# Minimal processing - make arciles resemble natural language
def article_process_text(text):
    return core_process_text(text, ERASE)

def summary_process_text(text):
    text = lower_first_token(text)
    text =  core_process_text(text, BLACK_NO_PER)
    tokens = [t.text if t.ent_type_ else t.text.lower() for t in nlp(text)]
    text = ' '.join(tokens)
    # try:
    #     tokens = [t.text if t.ent_type_ else t.text.lower() for t in nlp(text)]
    #     text = ' '.join(tokens)
    # except:
    #     print('failed', text)
    
    return text

def vocab_process_text(text):
    text = core_process_text(text, ERASE)
    tokens = [t.ent_type_ if t.ent_type_ else t.text.lower() for t in nlp(text)]
    text = ' '.join(tokens)
    return text

def core_process_text(text, ERASE):
    text = re.sub(ERASE, '', text) 
    text = re.sub(EMAIL_WORD, 'email', text)
    text = re.sub(EXT_PER, ext_per_repl, text)
    return text

def custom_ents(doc):
    # Add cutom entities
    spans = []
    ranges = []
    for label, expression in expressions.items():
        for match in re.finditer(expression, doc.text):
            start, end = match.span()
            start, end = tighten_bounds(start, end, doc.text)
            span = doc.char_span(start, end, label=label)
            if span and compatible_with_ranges(start, end, ranges): # check span does't overlap prior spans
                spans.append(span)
                ranges.append((start, end))
            
    # Add spans to the doc.ents
    doc.ents = list(doc.ents) + spans
    return doc


# CREATE CUSTOM NLP function from SpaCy
nlp = spacy.load("en_core_web_sm", disable=["tagger", "parser"])
nlp.add_pipe(custom_ents, name = 'custom', first=True)
nlp.add_pipe(nlp.create_pipe("merge_entities"))




