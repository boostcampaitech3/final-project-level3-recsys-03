import os

import torch
import wandb
from config import parse_args
import trainer
from dataloader import Preprocess
from sklearn.model_selection import train_test_split
from utils import setseeds


def main(config):
    wandb.login()

    setseeds(config)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    config.device = device

    preprocess = Preprocess(config)
    preprocess.load_train_data(config.file_name)
    train_data = preprocess.get_train_data()
    train_data, valid_data = train_test_split(train_data, train_size=config.ratio, shuffle=True)

    wandb.init(project="final_project", config=vars(config))
    trainer.run(config, train_data, valid_data)


if __name__ == "__main__":
    config = parse_args()
    os.makedirs(config.model_dir, exist_ok=True)
    main(config)