### Summarizer for Action Items ###

from data_util.data import Vocab
from data_util.batcher import TaskBatcher
from evaluate import TaskEvaluate
from model import TaskModel


class Summarizer:
    def __init__(self, vocab_path, model_path, model):
        self.vocab = vocab = Vocab(vocab_path)
        self.model_path = model_path
        self.model = model
        
    #TODO: make sure model has same vocab/opt as predictor
    #Maybe if batch is too big (>200?), separate into more batches

    def summarize(self, examples):
        batcher = TaskBatcher( # Batching obj
            examples=examples,
            vocab=self.vocab, 
            mode='train', 
            batch_size=len(examples), 
            single_pass=True
        )
        
        evaluator = TaskEvaluate(self.vocab, batcher, self.model, self.model_path)
        decoded_sents, ref_sents, context_sents, task_sents = evaluator.evaluate_batch()
        return decoded_sents
