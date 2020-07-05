import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
import time

import torch as T
import torch.nn as nn
import torch.nn.functional as F
from model import Model

from data_util import config, data
from data_util.batcher import Batcher
from data_util.data import Vocab
from train_util import *
from beam_search import *
from rouge import Rouge
import argparse

def get_cuda(tensor):
    if T.cuda.is_available():
        tensor = tensor.cuda()
    return tensor

class Evaluate(object):
    def __init__(self, vocab, batcher, model, model_path):
        self.vocab = vocab
        self.batcher = batcher
        self.model_path = model_path
        time.sleep(1)
        self.setup_valid(model)

    def setup_valid(self, model):
        self.model = model(self.vocab.size())
        self.model = get_cuda(self.model)
        checkpoint = T.load(os.path.join(config.save_model_path, self.model_path))
        self.model.load_state_dict(checkpoint["model_dict"])


    def print_original_predicted(self, decoded_sents, ref_sents, article_sents, loadfile):
        filename = "test_"+loadfile.split(".")[0]+".txt"
    
        with open(os.path.join("data",filename), "w") as f:
            for i in range(len(decoded_sents)):
                f.write("article: "+article_sents[i] + "\n")
                f.write("ref: " + ref_sents[i] + "\n")
                f.write("dec: " + decoded_sents[i] + "\n\n")

    def evaluate_batch(self):
        batch = self.batcher.next_batch()
        start_id = self.vocab.word2id(data.START_DECODING)
        end_id = self.vocab.word2id(data.STOP_DECODING)
        unk_id = self.vocab.word2id(data.UNKNOWN_TOKEN)
        decoded_sents = []
        ref_sents = []
        article_sents = []
        rouge = Rouge()
        while batch is not None:
            enc_batch, enc_lens, enc_padding_mask, enc_batch_extend_vocab, extra_zeros, ct_e = get_enc_data(batch)

            with T.autograd.no_grad():
                enc_batch = self.model.embeds(enc_batch)
                enc_out, enc_hidden = self.model.encoder(enc_batch, enc_lens)

            print('Summarizing Batch...')
            #-----------------------Summarization----------------------------------------------------
            with T.autograd.no_grad():
                pred_ids = beam_search(
                    enc_hidden, 
                    enc_out, 
                    enc_padding_mask, 
                    ct_e, 
                    extra_zeros, 
                    enc_batch_extend_vocab, 
                    self.model, 
                    start_id, 
                    end_id, 
                    unk_id,
                    self.vocab.size()
                )

            for i in range(len(pred_ids)):
                decoded_words = data.outputids2words(pred_ids[i], self.vocab, batch.art_oovs[i])
                decoded_words = " ".join(decoded_words)
                decoded_sents.append(decoded_words)
                abstract = batch.original_abstracts[i]
                article = batch.original_articles[i]
                ref_sents.append(abstract)
                article_sents.append(article)

            batch = self.batcher.next_batch()

        load_file = self.opt.load_model

        # if print_sents:
        #     self.print_original_predicted(decoded_sents, ref_sents, article_sents, load_file)

        # scores = rouge.get_scores(decoded_sents, ref_sents, avg = True)
        
        return decoded_sents, ref_sents, article_sents  # , scores


class TaskEvaluate(Evaluate):
    def __init__(self, vocab, batcher, model, model_path):
        super().__init__(vocab, batcher, model, model_path)

    def evaluate_batch(self):
        batch = self.batcher.next_batch()
        start_id = self.vocab.word2id(data.START_DECODING)
        end_id = self.vocab.word2id(data.STOP_DECODING)
        unk_id = self.vocab.word2id(data.UNKNOWN_TOKEN)
        decoded_sents = []
        ref_sents = []
        task_sents = []
        context_sents = []
        rouge = Rouge()
        while batch is not None:
            enc_batch, enc_seg_batch, enc_lens, enc_padding_mask, enc_batch_extend_vocab, extra_zeros, ct_e = get_enc_seg_data(batch)
            
            with T.autograd.no_grad():
                enc_batch = self.model.embeds(enc_batch)                                                    #Get embeddings for encoder input
                enc_seg_batch = self.model.seg_embeds(enc_seg_batch)
                enc_batch = T.cat([enc_batch, enc_seg_batch], dim=2)
                enc_out, enc_hidden = self.model.encoder(enc_batch, enc_lens)

            print('Summarizing Batch...')
            #-----------------------Summarization----------------------------------------------------
            with T.autograd.no_grad():
                pred_ids = beam_search(
                    enc_hidden, 
                    enc_out, 
                    enc_padding_mask, 
                    ct_e, 
                    extra_zeros, 
                    enc_batch_extend_vocab, 
                    self.model, 
                    start_id, 
                    end_id, 
                    unk_id,
                    self.vocab.size()
                )

            for i in range(len(pred_ids)):
                decoded_words = data.outputids2words(pred_ids[i], self.vocab, batch.art_oovs[i])
                decoded_sents.append(" ".join(decoded_words))
                ref_sents.append(batch.original_abstracts[i])
                task_sents.append(batch.original_tasks[i])
                context_sents.append(batch.original_contexts[i])


            batch = self.batcher.next_batch()

        # load_file = self.opt.load_model

        # if print_sents:
        #     self.print_original_predicted(decoded_sents, ref_sents, article_sents, load_file)

        # scores = rouge.get_scores(decoded_sents, ref_sents, avg = True)
        
        return decoded_sents, ref_sents, task_sents, context_sents

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", type=str, default="validate", choices=["validate","test"])
    parser.add_argument("--start_from", type=str, default="0020000.tar")
    parser.add_argument("--load_model", type=str, default=None)
    opt = parser.parse_args()

    if opt.task == "validate":
        saved_models = os.listdir(config.save_model_path)
        saved_models.sort()
        file_idx = saved_models.index(opt.start_from)
        saved_models = saved_models[file_idx:]
        for f in saved_models:
            opt.load_model = f
            eval_processor = Evaluate(config.valid_data_path, opt)
            eval_processor.evaluate_batch()
    else:   #test
        eval_processor = Evaluate(config.test_data_path, opt)
        eval_processor.evaluate_batch()
