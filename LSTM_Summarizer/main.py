import os
import sys
from data_util import config 
from summarizer import *

# from google.cloud import storage
# sys.path.append(os.path.abspath('models'))


summarizer  = Summarizer(
  vocab_path = os.path.join(config.log_root, 'data/vocab/vocab.txt'),
  model_path = os.path.join(config.log_root, "data/saved_models_2/0000360.tar"),
  model = TaskModel
)


def summarize(request):
  request_json = request.get_json(silent=True)
  contains_keys = [k in request_json for k in [CONT_KEY, TASK_KEY, SUM_KEY]]
  if not contains_keys:
    return 'request json missing necessary keys :('

  decoded = summarizer.summarize([request])
  return {'summary': decoded}


