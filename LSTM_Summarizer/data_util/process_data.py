 ### create a vocabulary from input files
import os
import time
import numpy as np
import pandas as pd
from nltk.tokenize import sent_tokenize

import config
from preprocess import *
from helper import parallel_map

# set random seed
np.random.seed(111)


# Constants
pr = '_processed'
tsv = '.tsv'

HEAD = 'headline'
TXT = 'text'

CONT_KEY = 'Context'
TASK_KEY = 'TaskSentence'
SUM_KEY = 'Summary'
COLS = [CONT_KEY, TASK_KEY, SUM_KEY]

col_func_map = {
  SUM_KEY:  summary_process_text, 
  CONT_KEY: article_process_text,
  TASK_KEY: article_process_text
}

def process_data(df, col_func, parallel=True): 
  for col, func in col_func.items():
    if parallel:
      df[col] = parallel_map(df[col].tolist(), func)
    else:
      df[col] = df[col].map(func)
  return df

def split_task_data(df):
  # shuffle
  df = df.sample(frac=1)
  ts = int(.2 * df.shape[0]) # test size
  vs = 300                   # val size
  # split
  val = df[:vs]
  test = df[vs:(ts+vs)]
  train = df[(ts+vs):]
  # write
  for d,n in zip([train, test, val], ['_train', '_test','_val']):
    d.to_csv(os.path.join(config.sum_path, 'task' + n + tsv), sep='\t', index=False)

def split_wiki_data(df):
  # shuffle
  df = df.sample(frac=1)
  vs = 300
  # split
  val = df[:vs]
  train = df[vs:]
  # write
  for d,n in zip([train, val], ['_train', '_val']):
    d.to_csv(os.path.join(config.sum_path, 'wiki' + n + tsv), sep='\t', index=False)

def split_wiki_text(text):
    sents = sent_tokenize(text)
    task_ = sents[-1]
    context_ = ' '.join(sents[:-1])
    return [task_, context_]

def process_wiki_data(df):
  df.rename(columns={HEAD: SUM_KEY}, inplace=True)
  df_ct = pd.DataFrame(df[TXT].map(split_wiki_text).tolist(), columns=[TASK_KEY, CONT_KEY])
  df = df[[SUM_KEY]].join(df_ct)
  return df

def main():
  start  = time.time()

  # process / split task data
  task = pd.read_csv(os.path.join(config.sum_path, 'task.tsv'), sep='\t')
  task = task.replace(np.nan, '')
  task = process_data(task[COLS], col_func_map)
  split_task_data(task)

  # process / split wikihow data
  wiki = pd.read_csv(os.path.join(config.sum_path, 'wiki.tsv'), sep='\t')
  wiki = wiki.dropna()
  wiki = process_wiki_data(wiki)
  wiki = process_data(wiki, col_func_map)
  split_wiki_data(wiki)

  end = time.time()
  elapsed = end - start
  print(f'SUCCESS. Finished in {round(elapsed/60,2)} minutes.')


if __name__ == "__main__":
    main()
