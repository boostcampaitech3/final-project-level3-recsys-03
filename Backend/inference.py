

def get_similar_fashion(image):



    '''
    image_IDs = model(image) # 모델을 통과시켜 유사한 이미지들의 ID값을 받는다.
    img_URL_list = csv[image_IDs][image_URL] # CSV 파일에서 해당 이미지의 URL을 불러온다
    '''
    # 임시로 만든 img_URL_list
    img_URL_list = ["https://image.msscdn.net/images/goods_img/20210401/1875663/1875663_1_500.jpg?t=20210401170705", 
    "https://image.msscdn.net/images/goods_img/20220302/2392494/2392494_1_500.jpg?t=20220428143207", 
    "https://image.msscdn.net/images/goods_img/20220302/2392493/2392493_1_500.jpg?t=20220428142946",
    "https://image.msscdn.net/images/goods_img/20210503/1934621/1934621_1_500.jpg?t=20210503162929"]

    return img_URL_list