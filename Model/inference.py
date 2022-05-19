import os

import torch
import PIL.Image as Image

from config import parse_args
import trainer
from dataloader import get_transforms, Preprocess


def main(config):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    config.device = device

    # 테스트 이미지
    image_path = os.path.join(config.test_dir, config.test_file_name)
    test_data = Image.open(image_path)
    transform = get_transforms()
    test_data = transform(test_data)
    
    # similarity를 구하기 위해 input image preprocessing
    preprocess = Preprocess(config)
    preprocess.load_train_data(config.file_name)
    train_data = preprocess.get_train_data()

    trainer.inference(config, test_data, train_data)


if __name__ == "__main__":
    config = parse_args()
    os.makedirs(config.model_dir, exist_ok=True)
    main(config)
