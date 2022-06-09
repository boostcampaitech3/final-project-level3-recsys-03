import os
import pandas as pd


def get_img_path(path):
    """
    이미지 경로 리스트 생성 함수
    article.csv에 없는 이미지를 찾기 위해 이미지 경로 생성 function 사용
    (ref: https://www.kaggle.com/code/hamditarek/similar-image-cnn-cosine-similarity)
    
    Parameters: 
    path(dtype=string): Path of directory
    
    Returns: 
    image_names(dtype=string): Full Image Path
    """
   
    image_names = []
   
    for dirname, _, filenames in os.walk(path):
        for filename in filenames:
            fullpath = os.path.join(dirname, filename)
            image_names.append(fullpath)
    
    return image_names


def del_article(config, df):
    """
    image를 갖고 있지 않는 article 제거 함수
    
    Parameters:
    df(dtype=object): pandas dataframe ("article_id", "product_type_name" feature 필요)

    Returns:
    df(dtype=object): image를 갖지 않는 article이 제거된 pandas dataframe ("str_id" feature 생성)
    """
    # indexing 목적으로 string으로 변환
    df.loc[:, "str_id"] = df["article_id"].astype(str)

    img_list = sorted(get_img_path(config.img_dir))

    # image가 없는 article을 제거
    non_img = list(set(df["str_id"]) - set(map(lambda x: x[-13:-4], img_list)))
    # 바로 value matching을 위해 search하면 속도가 너무 느려서 인덱스를 제거하는 방식을 사용
    non_img = sorted(non_img)
    article2id = {w: i for i, w in enumerate(df["str_id"])}
    non_idx = list(map(lambda x:article2id[x], non_img))
    df = df.drop(non_idx)

    return df


def del_class(config, df):
    """
    아기옷, 묶음상품, 악세서리 제거
    이미지 수가 limit_num보다 적은 class를 제거

    Parameters:
    df(dtype=object): pandas dataframe ("product_type_name", "index_group_name", "product_group_name" feature 필요)

    Returns:
    train_df(dtype=object): selection된 pandas dataframe
    """
    # 아기옷, 묶음상품 제거
    del_column = ["Baby/Children", "Divided"]
    df = df[~df["index_group_name"].isin(del_column)]
    # 악세서리 제거
    del_column = ["Accessories"]
    df = df[~df["product_group_name"].isin(del_column)]   
    # 이미지 수가 limit_num 보다 적은 class가 제거
    value=df["product_type_name"].value_counts()
    del_column = list(value[value < config.limit_num].keys())
    train_df = df[~df["product_type_name"].isin(del_column)]

    return train_df


def get_labels(config, df):
    """
    "product_type_name"를 사용하여 Label encoding

    Parameters:
    df(dtype=object): pandas dataframe ("product_type_name" feature 필요)

    Returns:
    df(dtype=object): image path가 추가된 pandas dataframe ("path" feaeture 생성)
    """
    product_list = list(df["product_type_name"].drop_duplicates()) 
    config.output_dim = len(product_list)
    config.product2id = {w: i for i, w in enumerate(product_list)}
    config.id2product = {i: w for i, w in enumerate(product_list)}   
    df["label"] = df["product_type_name"].apply(lambda x: config.product2id[x])
    # {"Vest top": 0, "Bra": 1, "Top": 2, "Trousers": 3, "Sweater": 4, "Underwear bottom": 5, 
    #  "T-shirt": 6, "Dress": 7, "Shirt": 8, "Shorts": 9, "Jacket": 10, "Skirt": 11, "Blouse": 12}

    return df


def get_sampling(config, df):
    """
    각 class별로 이미지 config.limit_size만큼 sampling하는 함수
    (Trousers(바지)는 2배 더 sampling)

    Parameters:
    df(dtype=object): pandas dataframe ("label" feature 필요)

    Returns:
    train_df(dtype=object): data sampling된 pandas dataframe
    """ 
    train_df = pd.DataFrame()

    for i in range(len(config.product2id)):
        # if i == 3:
        #     # label 3은 Trousers(바지). 하의 갯수가 작아서 바지는 2배 더 샘플링
        #     train_df = pd.concat([train_df, df[df["label"]==i].sample(n=(2*config.limit_num), replace=False)])
        train_df = pd.concat([train_df, df[df["label"]==i].sample(n=config.limit_num, replace=False)])

    return train_df  


def get_feature_img_path(config, df):
    """
    str_id를 사용하여 image path feature 추가

    Parameters:
    df(dtype=object): pandas dataframe ("str_id" feature 필요)

    Returns:
    df(dtype=object): image path가 추가된 pandas dataframe ("path" feaeture 생성)
    """
    df["path"] = df["str_id"].apply(lambda x: config.img_dir + "/0" + x[:2] + "/0" + x + ".jpg" )

    return df


def get_preprocess(config, df):
    """
    "product_type_name"를 사용하여 Label encoding

    Parameters:
    df(dtype=object): pandas dataframe 

    Returns:
    df(dtype=object): pandas dataframe (X="path", y="label")
    """
    # SettingWithCopyWarning 무시
    pd.set_option("mode.chained_assignment",  None)

    df = del_article(config, df)
    df = del_class(config, df)
    df = get_labels(config, df)
    df = get_sampling(config, df)
    df = get_feature_img_path(config, df)

    return df[["path", "label"]]