import pandas as pd
import numpy as np
import streamlit as st
import requests
from streamlit_cropper import st_cropper
from PIL import Image
from requests_toolbelt.multipart.encoder import MultipartEncoder
import io
import time

backend = "http://fastapi:8000/"

def getData(category, img_file, server_url = backend + 'getSimilarFashion'):
    # m = MultipartEncoder(fields={"category": category, "file": ("filename", img_file, "image/jpeg")}) # category 추가시 충돌 버그
    m = MultipartEncoder(fields={"file": ("filename", img_file, "image/jpeg")})

    r = requests.post(
        server_url, data=m, headers={"Content-Type": m.content_type}, timeout=8000
    )

    return r

# title 설정
st.title('비슷한 옷을 추천해줘')

# warning 제거 (https://discuss.streamlit.io/t/version-0-64-0-deprecation-warning-for-st-file-uploader-decoding/4465)
st.set_option('deprecation.showfileUploaderEncoding', False)

#소제목 설정
st.header("사진 업로드")

#사이드바에서 crop에 사용될 기능 설정(업로드 파일 형식/테두리 색상/image 비율 고정)
img_file = st.sidebar.file_uploader(label='사진 업로드', type=['png', 'jpg'])
box_color = st.sidebar.color_picker(label="테두리 색상", value='#000000')
aspect_ratio = None

#이미지 업로드시 crop 기능 실행
if img_file:
    img = Image.open(img_file)
    cropped_img = st_cropper(img, realtime_update=True, box_color=box_color,
                                aspect_ratio=aspect_ratio)
    
    # crop된 이미지를 출력 
    st.write("업로드 될 사진")
    image = cropped_img.thumbnail((500,500))
    st.image(cropped_img)

# 옷 종류 select 기능
category = '티셔츠'
category = st.selectbox('옷 종류',
                    ('티셔츠', '바지', '신발', '모자', '추가 예정'))

st.write('You selected:', category)

# 업로드 버튼을 누를 시 crop된 이미지를 확인, backend로 post 후에 image가 있는 dict를 받아옴
if st.button("업로드 완료"):
    if cropped_img :
        img_np_array = img_file
        # ConnectionError: HTTPConnectionPool 방지
        try:
            result = getData(category, img_np_array) 
            pass
        except:
            time.sleep(2)
            result = getData(category, img_np_array)
        col1, col2, col3, col4 = st.columns(4)
        col1.header("image0")
        col1.image(result.json()["image0"], use_column_width=True)
        col2.header("image1")
        col2.image(result.json()["image1"], use_column_width=True)
        col3.header("image2")
        col3.image(result.json()["image2"], use_column_width=True)
        col4.header("image3")
        col4.image(result.json()["image3"], use_column_width=True)

    else:
        st.write("좌측에서 이미지를 넣어주세요.")

# 이후 추가될 기능
st.write("무언가가 진행될 예정")


