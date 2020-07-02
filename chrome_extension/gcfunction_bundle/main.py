import sys
import os
import numpy
# from google.cloud import storage
sys.path.append(os.path.abspath('models'))
import preprocess
import nltk
nltk.download('punkt')
from nltk import sent_tokenize
import fasttext

def classify_text(request):
    print("request",request)
    request_json = request.get_json(silent=True)
    print("request_json", request_json)
    email_text = ""
    if request.args and 'message' in request.args:
        email_text = request.args.get('message')
    elif request_json and 'message' in request_json:
        email_text = request_json['message']
    else:
        return f'Something is wrong with request json. :('

    def preprocess_text(text):
        text = sent_tokenize(text)
        out = []
        final_text = ""
        for sentence in text:
            if type(sentence) == str:
                # clean text
                clean = preprocess.clean(sentence)
                # clean info
                clean = preprocess.clean_info(clean)

                out.append(clean)
                final_text+= " "+clean
            else:
                out.append("")
        return final_text
    
    email_text = preprocess_text(email_text)

    print("load fasttext model")
    ft_model = fasttext.load_model("models/best_ft_model.bin")
    # sentences = sent_tokenize(email_text)
    sentences = email_text
    res_dict = {"full_text": email_text}
    reqs = []
    certs = []
    for i in range(len(sentences)):
        prediction = ft_model.predict(sentences[i])
        if "1" in prediction[0][0]:
            reqs.append(sentences[i])
            certs.append(str(round(prediction[1][0], 2)))
        # res_dict[i] = {"sentence": sentences[i], 
        #                 "label": prediction[0][0],
        #                 "certainty": round(prediction[1][0], 2)
        #                 }
    
    res_dict["requests"] = reqs
    res_dict["certainty"] = certs
    return res_dict
