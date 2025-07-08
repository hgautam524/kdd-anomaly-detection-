import os

# List all KDD files you want to use
KDD_FILES = [
    'kddcup.data_10_percent_corrected',
    'kddcup.data.corrected',
    'kddcup.testdata.unlabeled',
    'kddcup.testdata.unlabeled_10_percent'
]

DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')
MODEL_DIR = os.path.join(os.path.dirname(__file__), '../models')