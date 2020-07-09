import os

log_root = "/Users/rowancassius/Desktop/capstone/LSTM_Summarizer"

sum_path        =  os.path.join(log_root, "data/sum")
vocab_path      =  os.path.join(log_root, "data/vocab")
embed_path      =  os.path.join(log_root, "data/embeddings")  
save_model_path =  os.path.join(log_root, "data/saved_models")  

# Hyperparameters
hidden_dim = 512
emb_dim = 200 # 256
batch_size = 200
max_enc_steps = 100		#99% of the articles are within length 55
max_dec_steps = 15		#99% of the titles are within length 15
beam_size = 4
min_dec_steps= 2
vocab_size = 50000

lr = 0.001
rand_unif_init_mag = 0.02
trunc_norm_init_std = 1e-4

eps = 1e-12
max_iterations = 500 #500000


save_model_path = "data/saved_models"
save_embedding_path = "data/embeddings"
results_path = "data/results"

intra_encoder = True
intra_decoder = True
