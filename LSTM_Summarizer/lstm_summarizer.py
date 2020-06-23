# Externalimports
import os
import importlib
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

# Internal imports
import model
import train
import evaluate
import train_util
import data_util.data
import data_util.batcher
import data_util.config

importlib.reload(model)
importlib.reload(train)
importlib.reload(evaluate)
importlib.reload(train_util)
importlib.reload(data_util.config)
importlib.reload(data_util.data)
importlib.reload(data_util.batcher)

from evaluate import *
from model import *
from train import *
from train_util import *
from data_util.data import *
from data_util.batcher import *

class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class Predictor:
    def __init__(self, vocab, task, load_model):
        self.vocab = vocab
        self.opt = Namespace(task = task, load_model = load_model)
        
#         self.model_path = opt.load_model
        
    #TODO: make sure model has same vocab/opt as predictor
    
    #Maybe if batch is too big (>200?), separate into more batches
    def predict(self, examples):
        task_batcher = TaskBatcher( # Batching obj
            examples=examples,
            vocab=self.vocab, 
            mode='train', 
            batch_size=len(examples), 
            single_pass=True)
        
        eval_processor = TaskEvaluate(self.vocab, task_batcher, self.opt)
        
        decoded_sents, ref_sents = eval_processor.evaluate_batch(model=TaskModel)
        return decoded_sents