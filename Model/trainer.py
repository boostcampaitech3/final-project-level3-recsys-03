import math
import os

import numpy as np
import torch
import wandb

from .dataloader import get_loaders, get_transforms
from .model import NeuralNetwork
from .optimizer import get_optimizer
from .scheduler import get_scheduler
from .feature_extraction import get_pretrained_model, get_extraction
from .utils import get_similarity, draw


def run(config, train_data, valid_data):
    train_loader, valid_loader = get_loaders(config, train_data, valid_data)

    # only when using warmup scheduler
    config.total_steps = int(math.ceil(len(train_loader.dataset) / config.batch_size)) * (
        config.n_epochs
    )
    config.warmup_steps = config.total_steps // 10

    model = get_model(config)
    optimizer = get_optimizer(model, config)
    scheduler = get_scheduler(optimizer, config)

    best_acc = -1
    early_stopping_counter = 0
    for epoch in range(config.n_epochs):

        print(f"Start Training: Epoch {epoch + 1}")

        ### TRAIN
        train_acc, train_loss = train(
            train_loader, model, optimizer, scheduler, config
        )

        ### VALID
        acc = validate(valid_loader, model, config)

        wandb.log(
            {
                "epoch": epoch,
                "train_loss": train_loss,
                "train_acc": train_acc,
                "valid_acc": acc,
            }
        )
        if acc > best_acc:
            best_acc = acc
            # torch.nn.DataParallel로 감싸진 경우 원래의 model을 가져옴
            model_to_save = model.module if hasattr(model, "module") else model
            save_checkpoint(
                {
                    "epoch": epoch + 1,
                    "state_dict": model_to_save.state_dict(),
                },
                config.model_dir,
                config.model_name,
            )
            early_stopping_counter = 0
        else:
            early_stopping_counter += 1
            if early_stopping_counter >= config.patience:
                print(
                    f"EarlyStopping counter: {early_stopping_counter} out of {config.patience}"
                )
                break

        # scheduler
        if config.scheduler == "plateau":
            scheduler.step(best_acc)


def train(train_loader, model, optimizer, scheduler, config):

    model.train()

    total_loss = 0.
    total_correct = 0.

    for step, (input, targets) in enumerate(train_loader):
        input = input.to(config.device)
        targets = targets.to(config.device)
 
        logits = model(input)
        _, preds = torch.max(logits, 1)

        loss = get_criterion(logits, targets)
        update_params(loss, model, optimizer, scheduler, config)

        if step % config.log_steps == 0:
            print(f"Training steps: {step} Loss: {str(loss.item())}")

        total_loss += loss * input.size(0)
        total_correct += torch.sum(preds == targets)

    # Train ACC
    acc = total_correct / len(train_loader.dataset)
    loss_avg = total_loss / len(train_loader.dataset)
    print(f"TRAIN ACC : {acc}")
    
    return acc, loss_avg


def validate(valid_loader, model, config):

    model.eval()
    total_correct = 0.
    
    with torch.no_grad():
        for step, (input, targets) in enumerate(valid_loader):
            input = input.to(config.device)
            targets = targets.to(config.device)
            
            logits = model(input)
            _, preds = torch.max(logits, 1)

            total_correct += torch.sum(preds == targets)

    # Valid ACC
    acc = total_correct / len(valid_loader.dataset)

    print(f"VALID ACC : {acc}\n")

    return acc


def inference(config, image_path, extracted_data):
    """
    test image를 feature extraction하여 target을 예측
    
    Parameters:
    image_path(dtype=str): test data path
    extracted_data(dtype=object) : brand, title, price, item_url, img_url, path, label, extraction_data
    """
    transform = get_transforms()
    pre_model = get_pretrained_model(config)
    model = load_model(config)
    sim_method = get_similarity(config)

    pre_model.eval()
    model.eval()

    with torch.no_grad():
        # input은 이미 cuda가 적용된 변수(dtype=torch.cuda.FloatTensor)
        input = get_extraction(config, image_path, transform, pre_model)
        logits = model(input)
        _, preds = torch.max(logits, 1)

        category = config.id2product[int(preds)]

        # similarity를 구함
        data = torch.tensor(extracted_data.iloc[:,7:].values)
        # "brand", "title", "price", "item_url", "img_url", "path", "label", "extraction_data"
        total_similarity = sim_method(input, data.to(config.device))

        # total_similarity 중 가장 similiarity가 높은 data k개 선정
        topk_idx = np.array(torch.topk(total_similarity, config.k)[1].to('cpu'))
        topk_data = extracted_data.iloc[topk_idx]
        topk_title =topk_data["title"].values
        topk_price = topk_data["price"].values
        topk_item_url = topk_data["item_url"].values
        topk_img_url = topk_data["img_url"].values

    return (category, topk_title, topk_price, topk_item_url, topk_img_url)


def get_model(config):
    """
    Load model and move tensors to a given devices.
    Returns:
    model(object): model
    """
    if config.model == "mlp":
        model = NeuralNetwork(config)

    model.to(config.device)

    return model


def get_criterion(pred, target):
    """
    loss 계산
    Parameters:
    pred(dtype=torch.float32): 예측값
    target(dtype=torch.float32): 정답

    Returns:
    loss(dtype=torch.float32): 계산된 loss
    """
    loss = torch.nn.CrossEntropyLoss()
    
    return loss(pred, target)


def update_params(loss, model, optimizer, scheduler, config):
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), config.clip_grad)
    optimizer.step()
    optimizer.zero_grad()


def save_checkpoint(state, model_dir, model_filename):
    print("saving model ...")
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    torch.save(state, os.path.join(model_dir, model_filename))


def load_model(config):
    model_path = os.path.join(config.model_dir, config.model_name)
    print("Loading Model from:", model_path)
    load_state = torch.load(model_path)
    model = get_model(config)

    # load model state
    model.load_state_dict(load_state["state_dict"], strict=True)

    print("Loading Model from:", model_path, "...Finished.")
    return model
