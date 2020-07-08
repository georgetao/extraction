import os
import sys
import json
import urllib.request
from google.cloud import storage

from summarizer import *

# Fetch model
model_file = '/tmp/model.tar'
storage_client = storage.Client()
bucket = storage_client.get_bucket('extraction_bucket_1')
blob = bucket.blob('saved_models/0000360.tar')
blob.download_to_filename(model_file)

# Create Summarizer
summarizer  = Summarizer(vocab_path = 'vocab.txt', model_path = model_file, model = TaskModel)

def summarize(request):
  request_json = request.get_json(silent=True)
  if "examples" not in request_json:
    return "request json missing key: examples"

  return json.dumps(summarizer.summarize(request_json["examples"]))
