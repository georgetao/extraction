import sys
import os
import numpy
# from google.cloud import storage
sys.path.append(os.path.abspath('models'))
import preprocess
import nltk
from nltk import sent_tokenize
import fasttext
import warnings
warnings.filterwarnings("ignore")

def classify_text(request):

    def preprocess_text(text):
        text = sent_tokenize(text)
        out = []
        for sentence in text:
            if type(sentence) == str:
                # clean text
                clean = preprocess.clean(sentence)
                # clean info
                clean = preprocess.clean_info(clean)

                out.append(clean)
            else:
                out.append("")
        return out

    sentences = preprocess_text(request)
    # sentences = sent_tokenize(request)
    print("SENTENCE:",sentences)
    print(type(sentences))
    email_text=sentences
    print("load fasttext model")
    ft_model = fasttext.load_model("models/best_ft_model.bin")
    print(email_text)
    res_dict = {"full_text": email_text}
    print(sentences)
    reqs = []
    certs = []
    for i in range(len(sentences)):
        prediction = ft_model.predict(sentences[i])
        if "1" in prediction[0][0]:
            reqs.append(sentences[i])
            certs.append(str(round(prediction[1][0], 2)))
        res_dict[i] = {"sentence": sentences[i], "label": prediction[0][0],"certainty": round(prediction[1][0], 2)}
    
    res_dict["requests"] = reqs
    res_dict["certainty"] = certs
    print(res_dict)
    return res_dict

text = "Please call me back tomorrow at 1234567890. I like the color blue. Also, please print out both copies."
classify_text(text)

import json
