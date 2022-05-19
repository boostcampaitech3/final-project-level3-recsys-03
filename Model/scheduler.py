from torch.optim.lr_scheduler import ReduceLROnPlateau


def get_scheduler(optimizer, config):
    if config.scheduler == "plateau":
        scheduler = ReduceLROnPlateau(
            optimizer, patience=10, factor=0.5, mode="max", verbose=True
            # patience : epoch 10 동안 개선되지 않으면 callback호출
            # factor : callback 호출시 lr을 절반 줄임
        )
        
    return scheduler
