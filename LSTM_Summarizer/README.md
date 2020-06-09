The link to the original github is: https://github.com/rohithreddy024/Text-Summarizer-Pytorch

##What to do##

Make sure your data is in .txt form and that the summary is in a different file than the entire sentence. Each line should be a new datapoint.

1. Make a folder called "data".

2. In "data", make two more folders called "unfinished" and "saved_models". We will use "saved_models" later to store our models.

3. In "data", copy your two .txt files. Name them "train.article.txt" (sentences) and "train.title.txt" (summaries).

4. Run the make_data_files jupyter notebook. It will create a "chunked" and "finished" folder in the "data" folder. Additionally, it will create a vocab file in "data".

5. PROBABLY NEED TO DO SOMETHING TO USE GPU

6. In the data_util/config.py file, change the num_iterations to the desired amount. Currently, I have it at 10 but the author recommends 500,000 iterations. Feel free to test changes to any of the other hyperparameters in config.py.

7. Run train jupyter notebook. Notice in the last section of code, you can change some values for train_mle. For the initial training, you should not need to. This notebook will create a saved model in the data/saved_models folder every 5000 iterations you run. You can change this value if you want to run less iterations for testing.

8. EVALUATION still not uploaded yet. 
