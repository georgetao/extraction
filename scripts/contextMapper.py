#!/usr/bin/python

# imports
import sys
import re
import numpy as np
from nltk.tokenize import sent_tokenize

from preprocess import *


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
            context_sents = [s for s in sents[:i] if not re.search(comp_regex, s)]
            context_sents = trim_sents(context_sents)
            context = '. '.join(context_sents)
        else:
            cs, context = '',''

        # print
        print(f'{task}\t{context}\t{cs}\t{ts}')
        
#         print(20*'=')
#         print('CONTEXT', clean_info(context))
#         print()
#         print('TASKSEN', clean_info(ts))
#         print()
        
        
    except:
        continue
