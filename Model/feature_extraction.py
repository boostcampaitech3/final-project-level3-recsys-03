from efficientnet_pytorch import EfficientNet
import torchvision.models as models
import torch
import torch.nn as nn


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
        pre_model =models.resnet34(pretrained=True)
        pre_model.fc = Identity()

    return pre_model.to(config.device)