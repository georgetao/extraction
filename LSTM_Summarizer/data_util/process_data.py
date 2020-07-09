 ### create a vocabulary from input files
import os
import time
import numpy as np
import pandas as pd

from data_util import config
from preprocess import *


# Constants
data_path = os.path.join(config.log_root, config.sum_path)
pr = '_processed'
tsv = '.tsv'

def process_data(filenames, col_func):
  for name in filenames:
    df = pd.read_csv(os.path.join(data_path, name + tsv), sep='\t')
    df.replace(np.nan, '', inplace=True)
    for col, func in col_func.items(): 
      df[col] = df[col].map(func)
    df.to_csv(os.path.join(data_path, name + pr + tsv))

def main():
  start  = time.time()
  # process task data
  process_data(
    filenames=['task_train', 'task_test', 'task_val'],
    col_func={
      'Summary': summary_process_text, 
      'Context': article_process_text,
      'TaskSentence': article_process_text}
  )
  # process wiki data
  process_data(
    filenames=['wiki_train', 'wiki_val'],
    col_func={'headline': summary_process_text, 'text': article_process_text}
  )
  end = time.time()
  elapsed = end - start
  print(f'SUCCESS. Finished in {round(elapsed/60,2)} minutes.')


if __name__ == "__main__":
    main()
