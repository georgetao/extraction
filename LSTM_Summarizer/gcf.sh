#!/bin/bash

# create archive
zip summarizer.zip

zip -u summarizer.zip beam_search.py
zip -u summarizer.zip evaluate.py
zip -u summarizer.zip evaluate.py
zip -u summarizer.zip main.py
zip -u summarizer.zip model.py
zip -u summarizer.zip summarizer.py
zip -u summarizer.zip train.py
zip -u summarizer.zip train_util.py
zip -u summarizer.zip __init__.py

zip -u summarizer.zip data/vocab/vocab3.txt 
zip -u summarizer.zip requirements.txt

zip -ur summarizer.zip data_util

