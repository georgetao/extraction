import os
import sys
import json
import urllib.request
from google.cloud import storage

from summarizer import *

# Fetch model
model_file = '/tmp/model.tar'
storage_client = storage.Client()
bucket = storage_client.get_bucket('extractionbucket')
blob = bucket.blob('task_summarizer_0000180.tar')
blob.download_to_filename(model_file)

# Create Summarizer
summarizer  = Summarizer(vocab_path='data/vocab/vocab3.txt', model_path=model_file, model=TaskModel)

def summarize(request):
  request_json = request.get_json(silent=True)
  if "examples" not in request_json:
    return "request json missing key: examples" 
  # if "mode" not in request_json:
  #   return "request json missing key: mode"

  return json.dumps(summarizer.summarize(request_json["examples"]))
