import os
import pickle

import torch
import modin.pandas as pd

from config import parse_args
import trainer


def main(config):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    config.device = device

    # 테스트 이미지 path
    image_path = os.path.join(config.test_dir, config.test_file_name)

    # similarity를 구하기 위해 feature extraction 적용된 데이터 load 
    data_path = os.path.join(config.asset_dir, config.asset_file)
    extracted_data = pd.read_csv(data_path)

    return trainer.inference(config, image_path, extracted_data)


if __name__ == "__main__":
    config = parse_args()
    os.makedirs(config.output_dir, exist_ok=True)
    main(config)