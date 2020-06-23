# import sys
# import os
import numpy
from google.cloud import storage
# sys.path.append(os.path.abspath('models'))
# import preprocess
from nltk import sent_tokenize
import fasttext

def classify_text(request):
    request_json = request.get_json(silent=True)
    email_text = ""
    if request.args and 'message' in request.args:
        email_text = request.args.get('message')
    elif request_json and 'message' in request_json:
        email_text = request_json['message']
    else:
        return f'Something is wrong with request json. :('
    # print("starting bucket stuff")
    # bucket_name = "extraction_bucket_1"
    # storage_client = storage.Client()
    # bucket = storage_client.get_bucket(bucket_name)
    # print("set up access to gcs bucket")
    # blob = bucket.blob("local packages")
    # blob.download_to_filename("/tmp/best_ft_model.bin")
    # print("load fasttext model")
    # ft_model = fasttext.load_model(open("/tmp/best_ft_model.bin"))
    
    return email_text.lower()
