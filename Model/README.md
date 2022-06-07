# 비슷한 옷을 추천해줘!

## feature extraction 후 데이터 저장
### 동작 순서
1. pretrained model([rembg](https://github.com/danielgatis/rembg))을 이용하여 image 배경제거
2. pretrained model resnet34를 이용한 feature extraction
3. fe_data(.csv 형식) 저장
### how to run
```
python3 feature_save.py
```
</br>

## Train
### 동작 순서
1. feature exraction된 데이터 load
2. MLP를 이용한 classification model training 진행
### how to run
```
python3 train.py
```

</br>

## Inference
### 동작 순서
1. fe_data(.csv 형식) load
2. input image 배경제거 후 resnet34를 이용하여 feature extraction
3. data 전체의 similarity를 계산하여 비슷한 옷 추천
### how to run
```
python3 inference.py
```