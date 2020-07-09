
import os
import time
import pandas as pd

from data_util import config
from helper import parallel_map
from data_util.preprocess import *
from keras.preprocessing.text import Tokenizer

# Manage Directories
data_path = os.path.join(config.log_root, config.sum_path)
vocab_path = os.path.join(config.log_root, config.vocab_path)


def select_vocab(vocab_name, n_wiki=300000, min_count=2):
  task = pd.read_csv(os.path.join(data_path, 'task_train.tsv'), sep='\t')
  wiki = pd.read_csv(os.path.join(data_path, 'wiki_train.tsv'), sep='\t')

  sents = pd.concat([wiki['text'][:n_wiki], task['TaskSentence'],task['Context']]).tolist()
  sents = parallel_map(sents, vocab_process_text)

  # fit tokenizer
  tokenizer = Tokenizer(lower=False, filters='')
  tokenizer.fit_on_texts(sents + list(ENT_TAGS))

  # write to vocab file
  path = os.path.join(vocab_path, vocab_name)
  vocab = pd.DataFrame(tokenizer.word_counts.items(), columns = ['word','count'])
  vocab = vocab[vocab['count'] >= min_count]['word']
  vocab.to_csv(path, index=False)

  # Report
  print(f'New vocab file written: {path}')


def main():
  start  = time.time()
  select_vocab(vocab_name='vocab3.txt')
  end = time.time()
  elapsed = end - start
  print(f'SUCCESS. Finished in {round(elapsed/60,2)} minutes.')
  

if __name__ == "__main__":
    main()