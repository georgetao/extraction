import os
import sys
import json
import urllib.request
from google.cloud import storage

from summarizer import *

# Fetch model
model_file = '/Users/rowancassius/Desktop/saved_models2/0000003.tar'
vocab_file = '/Users/rowancassius/Desktop/capstone/LSTM_Summarizer/data/vocab/vocab3.txt'

# Create Summarizer
summarizer  = Summarizer(vocab_path = vocab_file, model_path = model_file, model = TaskModel)

def summarize(request):
  request_json = request.get_json(silent=True)
  if "examples" not in request_json:
    return "request json missing key: examples"

  return json.dumps(summarizer.summarize(request_json["examples"]))
