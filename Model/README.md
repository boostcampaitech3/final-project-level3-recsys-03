# 비슷한 옷을 추천해줘!

## Baseline code
1. pretrained model resnet34를 이용한 feature extraction
2. MLP를 이용한 classification(class)
3. Inference에서 cosine similarity를 계산하여 비슷한 옷 추천


## How to run

```
python3 train.py
```

## Inference
```
python3 inference.py
```