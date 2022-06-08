from efficientnet_pytorch import EfficientNet
import torchvision.models as models
import torch
import torch.nn as nn
import csv

from tqdm import tqdm
import pandas as pd
import numpy as np
from rembg import remove
from PIL import Image
from .dataloader import get_transforms


class Identity(nn.Module):
    """
    pretrained model의 fully connected layer를 제거하여 feature extraction에 사용하기 위함
    (ref: https://discuss.pytorch.org/t/how-to-delete-layer-in-pretrained-model/17648)
    """
    def __init__(self):
        super(Identity, self).__init__()
        
    def forward(self, x):
        return x


def get_pretrained_model(config):
    if config.pre_model[:-3] == 'efficientnet':
        pre_model = EfficientNet.from_pretrained(config.pre_model)
    if config.pre_model == 'resnet34':
        pre_model = models.resnet34(pretrained=True)
        pre_model.fc = Identity()
    if config.pre_model == 'vgg19':
        pre_model = models.vgg19(pretrained=True)
        pre_model.classifier = Identity()

    return pre_model.to(config.device)


def get_extraction(config, path, transform, pre_model):
    """
    feature extraction 수행하는 함수
    
    Parameters:
    path(dtype=str): image data path
    transform(dtype=object): 이미지 resizing 등 torchvision transform
    pre_model : convolution까지만 적용하여 feature extraction
    
    Returns:
    extract_img(dtype=torch.cuda.FloatTensor): feature extraction된 tensor
    """
    # 이미지 한 개씩 적용
    img = Image.open(path).convert('RGB')
    # 이미지 segmentation
    seg_img = remove(img)
    # mask 부분을 제거
    seg_img = np.array(seg_img)
    seg_img = Image.fromarray(seg_img[:,:,:3])
    # 이미지 preprocessing
    img_tensor = transform(seg_img)
    img_tensor = torch.unsqueeze(img_tensor, dim=0)
    # pretrained model 적용하여 feature extraction
    extract_img = pre_model(img_tensor.to(config.device))
    del img_tensor

    return extract_img


def get_data(config, df):
    """
    feature extraction하여 데이터 생성하는 함수
    
    Parameters:
    df(dtype=object): 이미지에 대한 'path'를 가지고 있는 data frame
    
    Returns:
    data(dtype=np.array) : feature extraction된 data
    """
    path = df['path'].values
    data = torch.tensor([], dtype=torch.float32)
    pre_model = get_pretrained_model(config)
    transform = get_transforms()
    pre_model.eval()

    f = open("img_features.csv",'w',encoding='utf8')
    data_csv = csv.writer(f)
    data_csv.writerow(['path', 'features'])
    
    with torch.no_grad():
        for idx in tqdm(range(len(path))):
            extract_img = get_extraction(config, path[idx], transform, pre_model)
            # row로 data에 concat
            cpu_extract = extract_img.to('cpu')
            # GPU 메모리를 비우기 위해 Tensor delete 및 캐시 비우기 시행
            del extract_img
            torch.cuda.empty_cache()
            data = torch.cat([data, cpu_extract], dim=0)
            
            cpu_extract = torch.squeeze(cpu_extract, dim=0)
            data_csv.writerow([path[idx] , cpu_extract.detach().numpy().tolist()])

    data = np.array(data)

    return pd.DataFrame(data)