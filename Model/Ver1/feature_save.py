import os
import pickle
import torch
import numpy as np
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

    # inference 시 사용하기 위해 pickle로 저장 
    print("saving id2product ...")
    id2product_path = os.path.join(config.asset_dir, config.class_file)
    with open(id2product_path,'wb') as fw:
        pickle.dump(config.id2product, fw)
    
    print("saving path list ...")
    pickle_path = os.path.join(config.asset_dir, config.path_file)
    path_list = list(train_data['path'].values)
    with open(pickle_path,'wb') as fw:
        pickle.dump(path_list, fw)

    # feature extraction
    data = get_data(config, train_data)

    print("saving data ...")
    data_path = os.path.join(config.asset_dir, config.asset_file)
    np.save(data_path, data)  # numpy 저장 시 (.npy)

if __name__ == "__main__":
    config = parse_args()
    os.makedirs(config.asset_dir, exist_ok=True)
    main(config)