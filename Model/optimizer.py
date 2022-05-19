from torch.optim import Adam, AdamW


def get_optimizer(model, config):
    if config.optimizer == "adam":
        optimizer = Adam(model.parameters(), lr=config.lr, weight_decay=0.01)
    if config.optimizer == "adamW":
        optimizer = AdamW(model.parameters(), lr=config.lr, weight_decay=0.01)

    # 모든 parameter들의 grad값을 0으로 초기화
    optimizer.zero_grad()

    return optimizer
