import os
import modin.pandas as pd


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
    df["zero"] = df["category"].apply(lambda x: "0"*(6-len(str(x))))
    df["str_id"] = df["article_id"].astype(str)
    df["str_id"] = df["zero"] + df["str_id"]

    df = df.sort_values(by=["str_id"], ascending=[True])
    df = df.reset_index(drop=True)

    img_list = sorted(get_img_path(config.img_dir))[1:] # .DS_Store 때문에 2번째부터 적용

    # image가 없는 article을 제거
    non_img = list(set(df["str_id"]) - set(map(lambda x: x[(len(config.img_dir)+8):][:-4], img_list)))
    # 바로 value matching을 위해 search하면 속도가 너무 느려서 인덱스를 제거하는 방식을 사용
    non_img = sorted(non_img)
    article2id = {w: i for i, w in enumerate(df["str_id"])}
    non_idx = list(map(lambda x:article2id[x], non_img))
    df = df.drop(non_idx)

    return df


def get_labels(config, df):
    """
    "product_type_name"를 사용하여 Label encoding

    Parameters:
    df(dtype=object): pandas dataframe ("product_type_name" feature 필요)

    Returns:
    df(dtype=object): image path가 추가된 pandas dataframe ("path" feaeture 생성)
    """

    #product_list = list(df["category"].drop_duplicates()) # number of categories = 25 
    #config.product2id = {w: i for i, w in enumerate(product_list)}
    df["label"] = df["category"].apply(lambda x: config.product2id[x])

    df = df.reset_index(drop=True)
    
    return df


def get_feature_img_path(config, df):
    """
    str_id를 사용하여 image path feature 추가

    Parameters:
    df(dtype=object): pandas dataframe ("str_id" feature 필요)

    Returns:
    df(dtype=object): image path가 추가된 pandas dataframe ("path" feaeture 생성)
    """
    df["str_cate"] = df["category"].astype(str)
    df["path"] = config.img_dir + "/" 
    df["path"] += df["zero"] + df["str_cate"] + "/"  
    df["path"] += df["str_id"] + ".jpg"

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
    df = get_labels(config, df)
    df = get_feature_img_path(config, df)

    return df[["brand", "title", "price", "item_url", "img_url", "path", "label"]]