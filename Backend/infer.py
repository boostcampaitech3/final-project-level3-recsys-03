import sys
sys.path.append('../Model/')
import inference
import subprocess

def get_similar_fashion_model(image): # 이미지 찾기


    '''
    model = Model(category) # 카테고리에 맞는 모델 불러오기

    image_IDs = model(image) # 모델을 통과시켜 유사한 이미지들의 ID값을 받는다.
    img_URL_list = csv[image_IDs]['image_URL'] # CSV 파일에서 해당 이미지의 URL을 불러온다
    '''
    img_list = []
    k = subprocess.check_output("python Model/inference.py", shell=True)
    print(k)
    # 임시로 만든 img_URL_list
    img_URL_list = ["https://image.msscdn.net/images/goods_img/20210401/1875663/1875663_1_500.jpg?t=20210401170705", 
    "https://image.msscdn.net/images/goods_img/20220302/2392494/2392494_1_500.jpg?t=20220428143207", 
    "https://image.msscdn.net/images/goods_img/20220302/2392493/2392493_1_500.jpg?t=20220428142946",
    "https://image.msscdn.net/images/goods_img/20210503/1934621/1934621_1_500.jpg?t=20210503162929"]
    similar_fashion_list = img_URL_list
    #return {"image0" : similar_fashion_list[0], "image1" : similar_fashion_list[1], "image2" : similar_fashion_list[2], "image3" : similar_fashion_list[3]}
    return img_URL_list

def get_category_model(image): # 카테고리 찾기
    '''
    model = Model() 

    category = model(image) # 모델 결과 받기
    '''
    category = "바지" #임시 카테고리
    return category

