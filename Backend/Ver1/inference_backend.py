import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Model import config, inference

def get_similar_fashion_model(image): # 이미지 찾기
    

    '''
    model = Model(category) # 카테고리에 맞는 모델 불러오기

    image_IDs = model(image) # 모델을 통과시켜 유사한 이미지들의 ID값을 받는다.
    img_URL_list = csv[image_IDs]['image_URL'] # CSV 파일에서 해당 이미지의 URL을 불러온다
    '''
    conf = config.parse_args()
    img_list = []
    # 임시로 만든 img_URL_list
    category,img_URL_list = inference.main(conf)
    # similar_fashion_list = img_URL_list
    #return {"image0" : similar_fashion_list[0], "image1" : similar_fashion_list[1], "image2" : similar_fashion_list[2], "image3" : similar_fashion_list[3]}
    return (category,img_URL_list)

def get_category_model(image): # 카테고리 찾기
    '''
    model = Model() 

    category = model(image) # 모델 결과 받기
    '''
    category = "바지" #임시 카테고리
    return category

