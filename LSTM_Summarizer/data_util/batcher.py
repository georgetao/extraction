#Most of this file is copied form https://github.com/abisee/pointer-generator/blob/master/batcher.py

import queue as Queue
import time
from random import shuffle
from threading import Thread

import numpy as np
# import tensorflow as tf

from . import config
from . import data
from .preprocess import *

import random
random.seed(1234)

# Segment ids
SEGMENT = {'context':0, 'task':1, 'padding':2}

class Example(object):

  def __init__(self, article, abstract_sentences, vocab):
    # Get ids of special tokens
    start_decoding = vocab.word2id(data.START_DECODING)
    stop_decoding = vocab.word2id(data.STOP_DECODING)

    # Process the article
    article_words = article.split()
    if len(article_words) > config.max_enc_steps:
      article_words = article_words[:config.max_enc_steps]
    self.enc_len = len(article_words) # store the length after truncation but before padding
    self.enc_input = [vocab.word2id(w) for w in article_words] # list of word ids; OOVs are represented by the id for UNK token

    # Process the abstract
    abstract = ' '.join(abstract_sentences) # string
    abstract_words = abstract.split() # list of strings
    abs_ids = [vocab.word2id(w) for w in abstract_words] # list of word ids; OOVs are represented by the id for UNK token

    # Get the decoder input sequence and target sequence
    self.dec_input, _ = self.get_dec_inp_targ_seqs(abs_ids, config.max_dec_steps, start_decoding, stop_decoding)
    self.dec_len = len(self.dec_input)

    # If using pointer-generator mode, we need to store some extra info
    # Store a version of the enc_input where in-article OOVs are represented by their temporary OOV id; also store the in-article OOVs words themselves
    self.enc_input_extend_vocab, self.article_oovs = data.article2ids(article_words, vocab)

    # Get a verison of the reference summary where in-article OOVs are represented by their temporary article OOV id
    abs_ids_extend_vocab = data.abstract2ids(abstract_words, vocab, self.article_oovs)
    print(abs_ids_extend_vocab)

    # Get decoder target sequence
    _, self.target = self.get_dec_inp_targ_seqs(abs_ids_extend_vocab, config.max_dec_steps, start_decoding, stop_decoding)

    # Store the original strings
    self.original_article = article
    self.original_abstract = abstract
    self.original_abstract_sents = abstract_sentences

  def get_dec_inp_targ_seqs(self, sequence, max_len, start_id, stop_id):
    inp = [start_id] + sequence[:]
    target = sequence[:]
    if len(inp) > max_len: # truncate
      inp = inp[:max_len]
      target = target[:max_len] # no end_token
    else: # no truncation
      target.append(stop_id) # end token
    assert len(inp) == len(target)
    return inp, target


  def pad_decoder_inp_targ(self, max_len, pad_id):
    while len(self.dec_input) < max_len:
      self.dec_input.append(pad_id)
    while len(self.target) < max_len:
      self.target.append(pad_id)


  def pad_encoder_input(self, max_len, pad_id):
    while len(self.enc_input) < max_len:
      self.enc_input.append(pad_id)
    while len(self.enc_input_extend_vocab) < max_len:
      self.enc_input_extend_vocab.append(pad_id)

  def pad_encoder_segments(self, max_len, pad_id):
    while len(self.enc_seg) < max_len:
      self.enc_seg.append(pad_id)  


class TaskExample(Example):
  def __init__(self, context, task, summary, vocab):
    # Get ids of special tokens
    start_decoding = vocab.word2id(data.START_DECODING)
    stop_decoding = vocab.word2id(data.STOP_DECODING)

    # Process the context and the task
    context, task = nlp(context), nlp(task)
    self.entity_label_map = {**{e.text: e.label_ for e in context.ents}, 
                             **{e.text: e.label_ for e in task.ents}}
    
    # Reduce if necessary
    if len(context) + len(task) > config.max_enc_steps:
      t = min(len(task), config.max_enc_steps)
      c = max(0, config.max_enc_steps - t)
      # truncate
      task = task[:t]
      context = context[-c:] if c else []
    
    # create inputs
    self.enc_len = len(context) + len(task) # store the length after truncation but before padding
    self.enc_input = self.doc2ids(context, vocab) + self.doc2ids(task, vocab) #;OOVs are represented by the id for UNK token
    self.enc_seg = [SEGMENT['context'] for _ in context] + [SEGMENT['task'] for _ in task]

    # words:     'the', 'papers' 'are' 'wet' '.' 'dry' 'the papers' '.'
    # enc_input:   4      709      55   90   34    37    4   709    34
    # enc_seg:     0       0       0    0    0     1     1    1     1

    # If using pointer-generator mode, we need to store some extra info
    # Store a version of the enc_input where in-article OOVs are represented by their temporary OOV id; also store the in-article OOVs words themselves
    self.enc_input_extend_vocab, self.article_oovs = data.article2ids(
      data.doc2words(context) + data.doc2words(task), vocab
    )

    # Process the summary
    # Get a verison of the reference summary where in-article OOVs are represented by their temporary article OOV id
    sum_ids, sum_ids_extend_vocab = self.summary2ids_(summary, vocab)

    # Get the decoder input sequence and target sequence
    self.dec_input, _ = self.get_dec_inp_targ_seqs(sum_ids, config.max_dec_steps, start_decoding, stop_decoding)
    self.dec_len = len(self.dec_input)

    # Get decoder target sequence
    _, self.target = self.get_dec_inp_targ_seqs(
        sum_ids_extend_vocab, config.max_dec_steps, start_decoding, stop_decoding
    )
    # Store the original strings
    self.original_article = context.text + task.text
    self.original_context = context.text
    self.original_task = task.text
    self.original_abstract = summary       

  def word2id(self, word, vocab):
      if word in self.entity_label_map:
        return vocab.word2id(self.entity_label_map[word])
      return vocab.word2id(word) 

  def doc2ids(self, doc, vocab):
      return [self.word2id(w.text, vocab) if w.ent_type_ else 
              self.word2id(w.text.lower(), vocab) for w in doc]

  def summary2ids_(self, summary, vocab):
    'Returns an id list where in-article OOVs are represented by temporary ids'
    ids = []
    ids_extend = []
    unk_id = vocab.word2id(data.UNKNOWN_TOKEN)
    for w in nlp(summary):
      w_text = w.text if w.ent_type_ else w.text.lower() # lower non-entities
      i = vocab.word2id(w_text)
      if i == unk_id: # If w is an OOV word
        w_ = w_text.lower()
        is_oovs = np.array([[w_ is oov.lower(), w_ in oov.lower()] for oov in self.article_oovs]).T
        if np.any(is_oovs): # If w is an article OOV
          oov = self.article_oovs[np.argmax(is_oovs[0] if any(is_oovs[0]) else is_oovs[1])]
          vocab_idx = vocab.size() + self.article_oovs.index(oov)
          ids_extend.append(vocab_idx)
          ids.append(vocab.word2id(w.ent_type_ if w.ent_type_ else w_text))
        else: # If w is an out-of-article OOV
          w_ids = [vocab.word2id(v.text.lower()) for v in nlp(w_text)]
          ids_extend += w_ids
          ids += w_ids
      else:
        ids_extend.append(i)
        ids.append(i)
    assert len(ids) == len(ids_extend)    
    return ids, ids_extend 

    # summary token _s_ will be represented by article OOV token _a_ if
    #   * s.lower() == a.lower()
    #   * s.lower() in a.lower()

  def pretty_print(self):
    print(60*'=')
    print('CONTEXT:', self.original_context, '\n')
    print('TASK:   ', self.original_task, '\n')
    print('SUMMARY:', self.original_abstract)
    print(60*'=')


class Batch(object):
  def __init__(self, example_list, vocab, batch_size):
    self.batch_size = batch_size
    self.pad_id = vocab.word2id(data.PAD_TOKEN) # id of the PAD token used to pad sequences
    self.init_encoder_seq(example_list) # initialize the input to the encoder
    self.init_decoder_seq(example_list) # initialize the input and targets for the decoder
    self.store_orig_strings(example_list) # store the original strings


  def init_encoder_seq(self, example_list):
    # Determine the maximum length of the encoder input sequence in this batch
    max_enc_seq_len = max([ex.enc_len for ex in example_list])

    # Pad the encoder input sequences up to the length of the longest sequence
    for ex in example_list:
      ex.pad_encoder_input(max_enc_seq_len, self.pad_id)

    # Pad the segment inputs
    try:
      for ex in example_list:
        ex.pad_encoder_segments(max_enc_seq_len, SEGMENT['padding'])
    except AttributeError: pass

    # Initialize the numpy arrays
    # Note: our enc_batch can have different length (second dimension) for each batch because we use dynamic_rnn for the encoder.
    self.enc_batch = np.zeros((self.batch_size, max_enc_seq_len), dtype=np.int32)
    self.enc_seg_batch = np.zeros((self.batch_size, max_enc_seq_len), dtype=np.int32)
    self.enc_lens = np.zeros((self.batch_size), dtype=np.int32)
    self.enc_padding_mask = np.zeros((self.batch_size, max_enc_seq_len), dtype=np.float32)

    # Fill in the numpy arrays
    for i, ex in enumerate(example_list):
      self.enc_batch[i, :] = ex.enc_input[:]
      self.enc_lens[i] = ex.enc_len
      for j in range(ex.enc_len):
        self.enc_padding_mask[i][j] = 1

    # Try to fill in the segment arrays
    try:
      for i, ex in enumerate(example_list):
        self.enc_seg_batch[i, :] = ex.enc_seg[:]
    except AttributeError: pass

    # For pointer-generator mode, need to store some extra info
    # Determine the max number of in-article OOVs in this batch
    self.max_art_oovs = max([len(ex.article_oovs) for ex in example_list])
    # Store the in-article OOVs themselves
    self.art_oovs = [ex.article_oovs for ex in example_list]
    # Store the version of the enc_batch that uses the article OOV ids
    self.enc_batch_extend_vocab = np.zeros((self.batch_size, max_enc_seq_len), dtype=np.int32)
    for i, ex in enumerate(example_list):
      self.enc_batch_extend_vocab[i, :] = ex.enc_input_extend_vocab[:]

  def init_decoder_seq(self, example_list):
    # Pad the inputs and targets
    for ex in example_list:
      ex.pad_decoder_inp_targ(config.max_dec_steps, self.pad_id)

    # Initialize the numpy arrays.
    self.dec_batch = np.zeros((self.batch_size, config.max_dec_steps), dtype=np.int32)
    self.target_batch = np.zeros((self.batch_size, config.max_dec_steps), dtype=np.int32)
    # self.dec_padding_mask = np.zeros((self.batch_size, config.max_dec_steps), dtype=np.float32)
    self.dec_lens = np.zeros((self.batch_size), dtype=np.int32)

    # Fill in the numpy arrays
    for i, ex in enumerate(example_list):
      self.dec_batch[i, :] = ex.dec_input[:]
      self.target_batch[i, :] = ex.target[:]
      self.dec_lens[i] = ex.dec_len
      # for j in range(ex.dec_len):
      #   self.dec_padding_mask[i][j] = 1

  def store_orig_strings(self, example_list):
    self.original_articles = [ex.original_article for ex in example_list] # list of lists
    self.original_abstracts = [ex.original_abstract for ex in example_list] # list of lists
    self.original_tasks = [ex.original_task for ex in example_list]
    self.original_contexts = [ex.original_context for ex in example_list]
    # self.original_abstracts_sents = [ex.original_abstract_sents for ex in example_list] # list of list of lists


class Batcher(object):
  BATCH_QUEUE_MAX = 1000 # max number of batches the batch_queue can hold

  def __init__(self, examples, vocab, mode, batch_size, single_pass):
    self._examples = examples
    self._vocab = vocab
    self._single_pass = single_pass
    self.mode = mode  
    self.batch_size = batch_size
    # Initialize a queue of Batches waiting to be used, and a queue of Examples waiting to be batched
    self._batch_queue = Queue.Queue(self.BATCH_QUEUE_MAX)
    self._example_queue = Queue.Queue(self.BATCH_QUEUE_MAX * self.batch_size)

    # Different settings depending on whether we're in single_pass mode or not
    if single_pass:
      self._num_example_q_threads = 1 # just one thread, so we read through the dataset just once
      self._num_batch_q_threads = 1  # just one thread to batch examples
      self._bucketing_cache_size = 1 # only load one batch's worth of examples before bucketing; this essentially means no bucketing
      self._finished_reading = False # this will tell us when we're finished reading the dataset
    else:
      self._num_example_q_threads = 1 #16 # num threads to fill example queue
      self._num_batch_q_threads = 1 #4  # num threads to fill batch queue
      self._bucketing_cache_size = 1 #100 # how many batches-worth of examples to load into cache before bucketing

    # Start the threads that load the queues
    self._example_q_threads = []
    for _ in range(self._num_example_q_threads):
      self._example_q_threads.append(Thread(target=self.fill_example_queue))
      self._example_q_threads[-1].daemon = True
      self._example_q_threads[-1].start()
    self._batch_q_threads = []
    for _ in range(self._num_batch_q_threads):
      self._batch_q_threads.append(Thread(target=self.fill_batch_queue))
      self._batch_q_threads[-1].daemon = True
      self._batch_q_threads[-1].start()

    # Start a thread that watches the other threads and restarts them if they're dead

    # No more watching threads temporarily

    # if not single_pass: # We don't want a watcher in single_pass mode because the threads shouldn't run forever
    #   self._watch_thread = Thread(target=self.watch_threads)
    #   self._watch_thread.daemon = True
    #   self._watch_thread.start()

  def next_batch(self):
    # If the batch queue is empty, print a warning
    if self._batch_queue.qsize() == 0:
      # #tf.compat.v1.logging.warning('Bucket input queue is empty when calling next_batch. Bucket queue size: %i, Input queue size: %i', self._batch_queue.qsize(), self._example_queue.qsize())
      # if self._single_pass and self._finished_reading:
      if self._single_pass:
        #tf.compat.v1.logging.info("Finished reading dataset in single_pass mode.")
        return None

    batch = self._batch_queue.get() # get the next Batch
    return batch

  def fill_example_queue(self):
    input_gen = self.text_generator(data.example_generator(self._examples, self._single_pass))
    while True:
      try:
        (article, abstract) = next(input_gen) # read the next example from file. article and abstract are both strings.
        # print('ARTICLE:', article)
        # print('ARTICLE:', abstract)
        # print(30*'=')
      except StopIteration: # if there are no more examples:
        #tf.compat.v1.logging.info("The example generator for this example queue filling thread has exhausted data.")
        if self._single_pass:
          #tf.compat.v1.logging.info("single_pass mode is on, so we've finished reading dataset. This thread is stopping.")
          self._finished_reading = True
          break
        else:
          raise Exception("single_pass mode is off but the example generator is out of data; error.")

      # abstract_sentences = [sent.strip() for sent in data.abstract2sents(abstract)] # Use the <s> and </s> tags in abstract to get a list of sentences.
      abstract_sentences = [abstract.strip()]
      example = Example(article, abstract_sentences, self._vocab) # Process into an Example.
      self._example_queue.put(example) # place the Example in the example queue.

  def fill_batch_queue(self):
    while True:
      if self.mode == 'decode':
        # beam search decode mode single example repeated in the batch
        ex = self._example_queue.get()
        b = [ex for _ in range(self.batch_size)]
        self._batch_queue.put(Batch(b, self._vocab, self.batch_size))
      else:
        # Get bucketing_cache_size-many batches of Examples into a list, then sort
        inputs = []
        for _ in range(self.batch_size * self._bucketing_cache_size):
          inputs.append(self._example_queue.get())
        inputs = sorted(inputs, key=lambda inp: inp.enc_len, reverse=True) # sort by length of encoder sequence

        # Group the sorted Examples into batches, optionally shuffle the batches, and place in the batch queue.
        batches = []
        for i in range(0, len(inputs), self.batch_size):
          batches.append(inputs[i:i + self.batch_size])
        if not self._single_pass:
          shuffle(batches)
        for b in batches:  # each b is a list of Example objects
          self._batch_queue.put(Batch(b, self._vocab, self.batch_size))

  def watch_threads(self):
    while True:
      #tf.compat.v1.logging.info(
        # 'Bucket queue size: %i, Input queue size: %i',
        # self._batch_queue.qsize(), self._example_queue.qsize())

      time.sleep(60)

      for idx,t in enumerate(self._example_q_threads):
        if not t.is_alive(): # if the thread is dead
          #tf.compat.v1.logging.error('Found example queue thread dead. Restarting.')
          new_t = Thread(target=self.fill_example_queue)
          self._example_q_threads[idx] = new_t
          new_t.daemon = True
          new_t.start()
      for idx,t in enumerate(self._batch_q_threads):
        if not t.is_alive(): # if the thread is dead
          #tf.compat.v1.logging.error('Found batch queue thread dead. Restarting.')
          new_t = Thread(target=self.fill_batch_queue)
          self._batch_q_threads[idx] = new_t
          new_t.daemon = True
          new_t.start()


  def text_generator(self, example_generator):
    while True:
      e = next(example_generator) # e is a #tf.Example
      try:
        article_text, abstract_text = e
        # article_text = article_text.decode()
        # abstract_text = abstract_text.decode()    
      except ValueError:
        #tf.compat.v1.logging.error('Failed to get article or abstract from example')
        continue
      if len(article_text)==0: # See https://github.com/abisee/pointer-generator/issues/1
        ##tf.compat.v1.logging.warning('Found an example with empty article text. Skipping it.')
        continue
      else:
        yield (article_text, abstract_text)


# Keys for TaskBatcher
CONT_KEY = 'Context'
TASK_KEY = 'TaskSentence'
SUM_KEY = 'Summary'

class TaskBatcher(Batcher):
  def __init__(self, examples, vocab, mode, batch_size, single_pass):
    super().__init__(examples, vocab, mode, batch_size, single_pass)
    
  def fill_example_queue(self):
    input_gen = self.text_generator(data.example_generator(self._examples, self._single_pass))
    while True:
      try:
        context, task, summary = next(input_gen) # read the next example from file. article and abstract are both strings.
        # print('CONTEXT:', context)
        # print('TASK:', task)
        # print('SUMMARY:', summary)
        # print(30*'=')
      except StopIteration: # if there are no more examples:
        #tf.compat.v1.logging.info("The example generator for this example queue filling thread has exhausted data.")
        if self._single_pass:
          #tf.compat.v1.logging.info("single_pass mode is on, so we've finished reading dataset. This thread is stopping.")
          self._finished_reading = True
          break
        else:
          raise Exception("single_pass mode is off but the example generator is out of data; error.")

      example = TaskExample(context, task, summary, self._vocab) # Process into an Example.
      self._example_queue.put(example) # place the Example in the example queue.
        
  def text_generator(self, example_generator):
    while True:
      example = next(example_generator)
      try:
        context = example[CONT_KEY]
        task    = example[TASK_KEY]
        if SUM_KEY in example: #temporary fix
          summary = example[SUM_KEY]
        else: 
          summary = " " # 1 space summary if summary is absent
      except ValueError:
        #tf.compat.v1.logging.error('Failed to get context, task or abstract from example')
        continue
      if len(task)==0 or len(summary) == 0: 
        #tf.compat.v1.logging.warning('Found an example with empty article text. Skipping it.')
        continue
      else:
        yield context, task, summary       