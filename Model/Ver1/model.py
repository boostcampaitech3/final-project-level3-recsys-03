import torch
import torch.nn as nn


def init_weights(layer):
    """
    linear layer에 kaiming_uniform weight initialization 적용 (relu에 적합)
    (ref: https://localcoder.org/how-to-initialize-weights-in-pytorch)
    Parameters:
    layer(dtype=object): nn.Linear
    """
    if isinstance(layer, nn.Linear):
        nn.init.kaiming_uniform_(layer.weight, nonlinearity='relu')
        layer.bias.data.fill_(0.01)


class NeuralNetwork(nn.Module):
    def __init__(self,config):
        super(NeuralNetwork, self).__init__()
        self.mlp = nn.Sequential(
            nn.Linear(config.hidden_dim, config.hidden_dim),
            nn.ReLU(),
            nn.Linear(config.hidden_dim, config.output_dim),
        )
        self.mlp.apply(init_weights)

    def forward(self, x):
        logits = self.mlp(x)

        return logits
