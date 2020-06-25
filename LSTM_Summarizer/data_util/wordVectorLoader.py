# Most of the code from on https://github.com/chrisvdweth/ml-toolkit/blob/master/pytorch/utils/data/text/wordvectorloader.py

import numpy as np
import pandas as pd
import torch as T

import os
import csv
import timeit
import datetime

from data_util.config import rand_unif_init_mag

class WordVectorLoader:

    def __init__(self, embed_dim):
        self.embed_index = {}
        self.embed_dim = embed_dim

    def create_embedding_matrix(
            self, 
            embeddings_file_name, 
            word_to_index, 
            sep=' ', 
            init_random=True,
            print_each=10000, 
            verbatim=False):

        num_words = len(word_to_index)

        # Initialize embeddings matrix to handle unknown words
        if init_random:
            embed_mat = np.random.uniform(
                low=-rand_unif_init_mag, 
                high=rand_unif_init_mag, 
                size=(num_words, self.embed_dim))
        else:
            # initialize with zeros
            embed_mat = np.zeros((num_words, self.embed_dim))

        start = timeit.default_timer()
        with open(embeddings_file_name) as infile:
            for idx, line in enumerate(infile):
                elem = line.split(sep)
                word = elem[0]

                if verbatim is True:
                    if idx % print_each == 0:
                        print('[{}] {} lines processed'.format(datetime.timedelta(seconds=int(timeit.default_timer() - start)), idx), end='\r')

                if word not in word_to_index:
                    continue

                word_idx = word_to_index[word]

                if word_idx <= num_words:
                    embed_mat[word_idx] = np.asarray(elem[1:], dtype='float32')

        if verbatim == True:
            print()

        self.embed_mat = embed_mat

    def save_embed_mat(self, save_path):
        file = os.path.join(save_path, f"embedding_{self.embed_mat.shape[0]}_{self.embed_dim}.tar")
        T.save({'weight': T.Tensor(self.embed_mat)}, file)
        print('model saved at: \n', file)
