import os
import random
import numpy as np
import torch
import torch.nn as nn

from PIL import Image
import matplotlib.pyplot as plt


def setseeds(config):
    """
    랜덤 시드를 설정하여 매 코드를 실행할 때마다 동일한 결과를 얻게 합니다.
    """
    os.environ["PYTHONHASHSEED"] = str(config.seed)
    random.seed(config.seed)
    np.random.seed(config.seed)
    torch.manual_seed(config.seed)
    torch.cuda.manual_seed(config.seed)
    torch.backends.cudnn.deterministic = True


def get_similarity(config):
    """
    similarity 방법을 지정
    """
    if config.similarity == "cos":
        similarity = nn.CosineSimilarity(dim=1, eps=1e-6)

    return similarity


def draw(config, topk_path):
    """ 해당 이미지와 유사도가 높은 순대로 k개 이미지 출력하고 저장
    parameters:
    k(dtype=int): 이미지 갯수
    topk_path(dtype=list): 유사도가 높은 순 k개의 이미지 path를 담은 list
    returns:    
    """
    plt.figure(figsize=(40, 15))
    for i in range(config.k):
        plt.subplot(1, config.k, i+1)
        plt.imshow(Image.open(topk_path[i]))
    plt.tight_layout()
    #plt.show()

    # 터미널에서 이미지 출력이 안되므로 따로 저장
    path = os.path.join(config.output_dir, config.output_file_name)
    plt.savefig(path)
    print("Image download completed!")