import os
import pickle

import torch
import numpy as np

from .config import parse_args
from Model import trainer


def main(config):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    config.device = device

    # 테스트 이미지 path
    image_path = os.path.join(config.test_dir, config.test_file_name)

    # Load pickle 
    id2product_path = os.path.join(config.asset_dir, config.class_file)
    with open(id2product_path, 'rb') as fr:
        config.id2product = pickle.load(fr)

    pickle_path = os.path.join(config.asset_dir, config.path_file)
    with open(pickle_path, 'rb') as fr:
        path_list = pickle.load(fr)

    # similarity를 구하기 위해 feature extraction 적용된 데이터 load 
    data_path = os.path.join(config.asset_dir, config.asset_file)
    extracted_data = np.load(data_path)

    return trainer.inference(config, image_path, extracted_data, path_list)


if __name__ == "__main__":
    config = parse_args()
    os.makedirs(config.model_dir, exist_ok=True)
    main(config)