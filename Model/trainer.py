import math
import os

import numpy as np
import torch
import wandb

from dataloader import get_loaders
from model import NeuralNetwork
from optimizer import get_optimizer
from scheduler import get_scheduler
from feature_extraction import get_pretrained_model
from utils import get_similarity, draw


def run(config, train_data, valid_data):
    train_loader, valid_loader = get_loaders(config, train_data, valid_data)

    # only when using warmup scheduler
    config.total_steps = int(math.ceil(len(train_loader.dataset) / config.batch_size)) * (
        config.n_epochs
    )
    config.warmup_steps = config.total_steps // 10

    pre_model = get_pretrained_model(config)
    model = get_model(config)
    optimizer = get_optimizer(model, config)
    scheduler = get_scheduler(optimizer, config)

    best_acc = -1
    early_stopping_counter = 0
    for epoch in range(config.n_epochs):

        print(f"Start Training: Epoch {epoch + 1}")

        ### TRAIN
        train_acc, train_loss = train(
            train_loader, pre_model, model, optimizer, scheduler, config
        )

        ### VALID
        acc = validate(valid_loader, pre_model, model, config)

        ### TODO: model save or early stopping
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
            # torch.nn.DataParallel로 감싸진 경우 원래의 model을 가져옵니다.
            model_to_save = model.module if hasattr(model, "module") else model
            save_checkpoint(
                {
                    "epoch": epoch + 1,
                    "state_dict": model_to_save.state_dict(),
                },
                config.model_dir,
                "model.pt",
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


def train(train_loader, pre_model, model, optimizer, scheduler, config):

    model.train()

    total_loss = 0.
    total_correct = 0.

    for step, (images, targets) in enumerate(train_loader):
        images = images.to(config.device)
        targets = targets.to(config.device)
        input = pre_model(images)
        
        logits = model(input)
        _, preds = torch.max(logits, 1)

        loss = get_criterion(logits, targets)
        update_params(loss, model, optimizer, scheduler, config)

        if step % config.log_steps == 0:
            print(f"Training steps: {step} Loss: {str(loss.item())}")

        total_loss += loss * images.size(0)
        total_correct += torch.sum(preds == targets)

    # Train ACC
    acc = total_correct / len(train_loader.dataset)
    loss_avg = total_loss / len(train_loader.dataset)
    print(f"TRAIN ACC : {acc}")
    return acc, loss_avg


def validate(valid_loader, pre_model, model, config):

    model.eval()

    total_correct = 0.

    for step, (images, targets) in enumerate(valid_loader):
        images = images.to(config.device)
        targets = targets.to(config.device)
        input = pre_model(images)
        
        logits = model(input)
        _, preds = torch.max(logits, 1)

        total_correct += torch.sum(preds == targets)

    # Valid ACC
    acc = total_correct / len(valid_loader.dataset)

    print(f"VALID ACC : {acc}\n")

    return acc


def inference(config, test_data, train_data):
    # test image를 feature extraction하여 target을 예측
    pre_model = get_pretrained_model(config)
    model = load_model(config)

    model.eval()

    input = pre_model(test_data.unsqueeze(dim=0).to(config.device))
    logits = model(input)
    _, preds = torch.max(logits, 1)

    print("predict :", config.id2product[int(preds)])

    # similarity를 구하기 위해서 train dataset 사용
    # 같은 label을 갖는 데이터셋을 dataloader에 넣어서 batch 단위로 simialrity 계산
    dataset = train_data[train_data["label"]==int(preds)]

    _, test_loader = get_loaders(config, None, dataset)

    sim_method = get_similarity(config)
    total_similarity = torch.tensor([]).to(config.device)

    for step, (images, _) in enumerate(test_loader):
        images = images.to(config.device)
        features = pre_model(images)
        
        similarity_tensor = sim_method(input, features)
        total_similarity = torch.cat([total_similarity, similarity_tensor], dim=0)

    # total_similarity 중 가장 similiarity가 높은 data k개의 path로 image 생성
    topk_idx = np.array(torch.topk(total_similarity, config.k)[1].to('cpu'))
    topk_path = dataset.iloc[topk_idx].path.values

    draw(config, topk_path)


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
