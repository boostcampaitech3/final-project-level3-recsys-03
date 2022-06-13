![https://user-images.githubusercontent.com/91198452/172392408-a51b15f0-fe68-4671-989b-e843b0c71bd9.jpg](https://user-images.githubusercontent.com/91198452/172392408-a51b15f0-fe68-4671-989b-e843b0c71bd9.jpg)

## 1️⃣ Introduction

### 1) Background

사람들은 패션 아이콘처럼 멋진 모습으로 자신을 표현하고 싶어합니다. 하지만, 유명 인플루언서들이 착용하는 럭셔리 브랜드 제품은 일반 소비자가 구매하여 즐기기에는 가격대가 높습니다. ‘비슷한 옷을 추천해줘!’ 프로젝트는 원하는 스타일의 제품을 합리적인 가격으로 구매하고 싶어하는 소비자들을 위하여 비슷한 스타일의 제품을 제공하는 웹 서비스를 만들어보고자 기획되었습니다.

### 2) Project Objective

- 입력된 이미지로부터 패션 아이템의 특성을 판별하기 위한 Feature를 정의하고 추출합니다.
- 유사도 비교를 통해 컨텐츠 기반의 Top-K 추천 목록을 생성합니다.
- Streamlit과 FastAPI를 적용하여 배포 가능한 형태의 웹 서비스를 개발합니다.

![https://user-images.githubusercontent.com/91198452/172392673-f2b006c0-c0ae-4616-9045-6b506baa398d.png](https://user-images.githubusercontent.com/91198452/172392673-f2b006c0-c0ae-4616-9045-6b506baa398d.png)

---

## 2️⃣ Service Architecture

### 1) Project Tree

```
📦final-project-level3-recsys-03
 ┣ 📂Backend
 ┃ ┣ 📜README.md
 ┃ ┣ 📜dockerfile
 ┃ ┣ 📜inference_backend.py
 ┃ ┣ 📜main.py
 ┃ ┗ 📜requirements.txt
 ┣ 📂Data
 ┃ ┣ 📜README.md
 ┃ ┣ 📜data_crawling.py
 ┃ ┗ 📜data_load.py
 ┣ 📂Frontend
 ┃ ┣ 📜Dockerfile
 ┃ ┣ 📜README.md
 ┃ ┣ 📜demo.py
 ┃ ┗ 📜requirements.txt
 ┣ 📂Model
 ┃ ┣ 📜README.md
 ┃ ┣ 📜config.py
 ┃ ┣ 📜dataloader.py
 ┃ ┣ 📜feature_extraction.py
 ┃ ┣ 📜feature_save.py
 ┃ ┣ 📜inference.py
 ┃ ┣ 📜model.py
 ┃ ┣ 📜optimizer.py
 ┃ ┣ 📜preprocess.py
 ┃ ┣ 📜scheduler.py
 ┃ ┣ 📜train.py
 ┃ ┣ 📜trainer.py
 ┃ ┗ 📜utils.py
 ┣ 📜.gitignore
 ┣ 📜CONTRIBUTING.md
 ┣ 📜README.md
 ┣ 📜docker-compose.yml
 ┗ 📜requirements.txt
```

### 2) System Architecture
![Untitled](https://user-images.githubusercontent.com/78737997/173265755-a8212f88-3230-4573-92ab-9d96384e608f.jpeg)

1. Streamlit 기반의 웹 서비스가 시작되면 웹 페이지에 시작 화면이 전시됩니다.
2. 사용자는 서비스의 [이미지 업로드] 버튼을 클릭하여 입고 싶은 스타일의 사진을 업로드 합니다.
3. 사용자는 서비스의 [Image Crop] 기능을 사용하여 사진에서 원하는 제품 영역을 선택합니다.
4. Crop Image는 FastAPI를 통해 Modeling Component에 전달됩니다.
5. Modeling 모듈에서는 전처리(배경제거) → 특징추출 → multi-classification → 유사도 분석을 수행하고 해당 제품의 유형 정보와 추천 아이템 목록을 추론합니다.
6. 추론된 제품 유형 정보와 추천 아이템 목록은 FastAPI를 통해 웹 서비스로 전송됩니다.
7. 서비스는 데이터 저장소로부터 추천 아이템 ID 목록에 해당하는 URL과 제품 image 정보를 추출하여 웹 페이지에 전시합니다.

---

## 3️⃣ DataSet

### 1) 데이터셋 구성 파이프라인

![image](https://user-images.githubusercontent.com/78737997/173267641-dea2bd15-a18e-42fb-ad9c-869d2772d287.png)

### 2) 데이터셋 수집

- 1차 : Kaggle Personalized Fashion Recommendations 데이터셋 활용
    - [https://www.kaggle.com/c/h-and-m-personalized-fashion-recommendations](https://www.kaggle.com/c/h-and-m-personalized-fashion-recommendations)
- 2차 : 크롤링 데이터셋 적용
    - 무신사닷컴, [www.musinsa.com](http://www.musinsa.com/)

---

## 4️⃣ Modeling

### 1) Flow Chart

![https://user-images.githubusercontent.com/91198452/172393139-aa62568e-a3b8-4a2a-adc9-0325376cc3db.png](https://user-images.githubusercontent.com/91198452/172393139-aa62568e-a3b8-4a2a-adc9-0325376cc3db.png)

### 2) Preprocessing

- 배경 제거 Segmentation을 위해 UNet 기반 rembg 적용
- 3 x 224 x 224 image resizing
- Data normalization

### 3) Feature Extraction

- ResNet34의 convolution part 적용
- 3 x 224 x 224 크기의 image로부터 1 x 512 크기의 feature vector 추출

### 4) Multi-Classification

- 512-512-13 구조의 Multi layer perceptron 적용
- Test dataset 기준 accuracy 78.12%

### 5) Top-K Recommender

- 저장된 feature data들과 cosine similarity를 계산하여 Top-K 이미지 선택

---

## 5️⃣Product Serving

### 1) SW 구성

![https://user-images.githubusercontent.com/91198452/172394318-980681d3-cb23-44db-af1b-63d94f8869fb.png](https://user-images.githubusercontent.com/91198452/172394318-980681d3-cb23-44db-af1b-63d94f8869fb.png)

### 2) FrontEnd (Streamlit)

- 사용자 인터페이스 제공 : 이미지 업로드, 크롭, 전시 등
- 서비스 결과 전시 : 제품 유형, 유사 제품 이미지, 제품 링크, 가격 등

### 3) BackEnd (FastAPI)

- Model 과 FrontEnd 를 연결
- Client로부터 데이터를 수신하여 Inference 모듈을 호출
- Inference 모듈로부터 추론 결과를 수신하여 Client로 전송

### 4) Docker

- FrontEnd와 BackEnd가 각각 독립된 Docker container 상에서 실행
- Docker-compose를 이용해 즉시 실행 가능

---

## 6️⃣ **How to Run**

You need install [Docker](https://www.docker.com/) first

### run

```
docker-compose build
docker-compose up
```

### delete container

```
docker-compose down
```

### without docker

```
cd Backend/
python main.py

cd ../Frontend
streamlit run demo.py
```

## 7️⃣ **Demo (시연 영상)**

- 시연영상

![시연영상](https://user-images.githubusercontent.com/78737997/173265924-5563255e-480d-467b-a2df-5383cf8586ac.gif)

## 8️⃣ Reference

- [https://www.kaggle.com/code/hamditarek/similar-image-cnn-cosine-similarity](https://www.kaggle.com/code/hamditarek/similar-image-cnn-cosine-similarity)

## 9️⃣ 팀원 소개

| 이름 | GitHub | 역할 |
| --- | --- | --- |
| 강영석 | [kysuk05](https://github.com/kysuk05)  | 프론트엔드(streamlit), GitHub, 백엔드 |
| 김수희 | [Kimsuhhee](https://github.com/Kimsuhhee) | 데이터베이스, 크롤링, 전처리  |
| 김예지 | [imyjk729](https://github.com/imyjk729) | 전처리, 특징추출, Top-K 추천 |
| 이현우 | [harrier999](https://github.com/harrier999)  | 백엔드(FastAPI), Docker, 크롤링 |
| 홍수연 | [sparklingade](https://github.com/sparklingade)  | PM, 전처리, 크롤링 |
