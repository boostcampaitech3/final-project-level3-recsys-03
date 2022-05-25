import os
import random

import numpy as np
import pandas as pd
import tqdm

import torch
from torchvision import transforms
from torchvision.transforms import Resize, ToTensor, Normalize, RandomHorizontalFlip
from PIL import Image

from preprocess import get_preprocess


class Preprocess:
    def __init__(self, config):
        self.config = config
        self.train_data = None
        self.test_data = None

    def get_train_data(self):
        return self.train_data

    def get_test_data(self):
        return self.test_data 

    def __preprocessing(self, df):
        df = get_preprocess(self.config, df)

        return df

    def load_data_from_file(self, file_name):
        csv_file_path = os.path.join(self.config.data_dir, file_name)
        df = pd.read_csv(csv_file_path) 
        df = self.__preprocessing(df)   

        return df  

    def load_train_data(self, file_name):
        self.train_data = self.load_data_from_file(file_name)

    def load_test_data(self, file_name):
        self.test_data = self.load_data_from_file(file_name)


class HandMDataset(torch.utils.data.Dataset):
    def __init__(self, img):
        self.X = img['path']
        self.y = img['label']
        self.transform = get_transforms()
    
    def __getitem__(self, index):
        image = Image.open(self.X.iloc[index]).convert('RGB')
        label = self.y.iloc[index]

        if self.transform:
            image = self.transform(image) # torchvision 

        return image, torch.tensor(label)

    def __len__(self):
        return len(self.X)


class ExtractionDataset(torch.utils.data.Dataset):
    """
    classfication 단게에서 사용
    """
    def __init__(self, img):
        self.data = img[:, :-1]
        self.label = img[:, -1]
    
    def __getitem__(self, index):
        X = torch.tensor(self.data[index], dtype=torch.float32)
        y = torch.tensor(self.label[index], dtype=torch.int64)

        return X, y

    def __len__(self):
        return len(self.data)


def get_transforms():
    transform = transforms.Compose([Resize((224, 224), Image.BILINEAR),
                                    # RandomHorizontalFlip(p=0.3), # randomly H_flip images
                                    ToTensor(),
                                    Normalize((0.5), (0.5)),
                                    ])
    return transform


def get_loaders(config, train, valid):
    """
    Split data into two parts with a given ratio.
    
    Parameters:
    valid(dtype=): data
    ratio(dtype=float): train dataset 비율
    shuffle(dtype=boolean): 데이터를 섞을 것인지 결정

    Returns:
    data_1(dtype=): train_dataset
    data_2(dtype=): valid_dataset
    """
    pin_memory = False
    train_loader, valid_loader = None, None

    if train is not None:
        trainset = ExtractionDataset(train)
        train_loader = torch.utils.data.DataLoader(
            trainset,
            shuffle=True,
            batch_size=config.batch_size,
            pin_memory=pin_memory,
        )
    if valid is not None:
        valset = ExtractionDataset(valid)
        valid_loader = torch.utils.data.DataLoader(
            valset,
            shuffle=False,
            batch_size=config.batch_size,
            pin_memory=pin_memory,
        )

    return train_loader, valid_loader
