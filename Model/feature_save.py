import os
import torch
import numpy as np
import modin.pandas as pd

from config import parse_args
from dataloader import Preprocess
from utils import setseeds
from feature_extraction import get_data


def main(config):

    setseeds(config)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    config.device = device

    preprocess = Preprocess(config)
    preprocess.load_train_data(config.file_name)
    train_data = preprocess.get_train_data()

    # feature extraction
    data = get_data(config, train_data)

    # meta data, feature extraction된 data를 concatenate
    train_df = pd.concat([train_data, data], axis=1)

    print("saving data ...")
    data_path = os.path.join(config.asset_dir, config.asset_file)
    train_df.to_csv(data_path, index=False) # csv 저장

if __name__ == "__main__":
    config = parse_args()
    os.makedirs(config.asset_dir, exist_ok=True)
    main(config)