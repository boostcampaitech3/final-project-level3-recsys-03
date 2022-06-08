import os
import torch
import numpy as np
import pandas as pd

from config import parse_args
from dataloader import Preprocess
from utils import setseeds
from feature_extraction import get_data
import sys
sys.path.append('/opt/ml/final-project-level3-recsys-03/Data')
import data_query

def main(config):

    setseeds(config)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    config.device = device

    preprocess = Preprocess(config)
    preprocess.load_train_data(config.file_name)
    train_data = preprocess.get_train_data()

    print("saving train data ...")
    data_path = os.path.join(config.asset_dir, config.asset_file)
    train_data.to_csv(data_path, index=False) # csv 저장

    # feature extraction
    data = get_data(config, train_data)

    to_bigquery = pd.read_csv("./img_features.csv")
    data_query.load_features_to_bigquery(to_bigquery,'musinsadb.img_features')



if __name__ == "__main__":
    config = parse_args()
    os.makedirs(config.asset_dir, exist_ok=True)
    main(config)