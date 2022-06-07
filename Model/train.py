import os

import torch
import modin.pandas as pd
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

    data_path = os.path.join(config.asset_dir, config.asset_file)
    data = pd.read_csv(data_path)
    # "brand", "title", "price", "item_url", "img_url", "path", "label", "extraction_data"
    train_data, valid_data = train_test_split(data.iloc[:,6:], train_size=config.ratio, shuffle=True)

    wandb.init(project="final_project", config=vars(config))
    trainer.run(config, train_data, valid_data)


if __name__ == "__main__":
    config = parse_args()
    os.makedirs(config.model_dir, exist_ok=True)
    data_path = os.path.join(config.asset_dir, config.asset_file)
    main(config)