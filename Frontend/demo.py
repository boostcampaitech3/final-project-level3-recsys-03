from xml.etree.ElementInclude import default_loader
import pandas as pd
import numpy as np
import streamlit as st
import requests
from streamlit_cropper import st_cropper
from PIL import Image
from requests_toolbelt.multipart.encoder import MultipartEncoder
import io
import time
import argparse
from yaml import parse

parser = argparse.ArgumentParser(description="--docker=True/False, default=False")
docker_choices = ('True', 'Fasle')
parser.add_argument('--docker', choices=docker_choices, default='False', help="--docker=True/False, default=False")

args = parser.parse_args()

if args.docker=='False':
    backend = "http://localhost:8000/"
elif args.docker=='True':
    backend = "http://fastapit:8000/"

def convert_pil_image_to_byte_array(img):
    img_byte_array = io.BytesIO()
    img.save(img_byte_array, format='JPEG', subsampling=0, quality=100)
    img_byte_array = img_byte_array.getvalue()
    return img_byte_array


def getData(img_file, server_url = backend + 'getSimilarFashion'):
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
img_file = st.file_uploader(label='', type=['png', 'jpg'])
aspect_ratio = None


#이미지 업로드시 crop 기능 실행
if img_file:
    img = Image.open(img_file)
    cropped_img = st_cropper(img, realtime_update=True, box_color='#000000',
                                aspect_ratio=aspect_ratio)
    
    # crop된 이미지를 출력 
    st.write('업로드 될 사진')
    image = cropped_img.thumbnail((500,500))
    st.image(cropped_img)

# 업로드 버튼을 누를 시 crop된 이미지를 확인, backend로 post 후에 image가 있는 dict를 받아옴
if st.button("업로드 완료"):
    if cropped_img :
        with st.spinner('로딩중...'):
            cropped_img_bytearray = convert_pil_image_to_byte_array(cropped_img)
            img_np_array = cropped_img_bytearray
            # ConnectionError: HTTPConnectionPool 방지
            try:
                result = getData(img_np_array) 
                pass
            except:
                time.sleep(2)
                result = getData(img_np_array)
        
        st.header("비슷한 이미지 결과")
        st.write('옷 종류:', result.json()["category"])
        
        col1, col2, col3, col4 ,col5 = st.columns(5)
        
        col1.image(result.json()["image0"], use_column_width=True)
        col2.image(result.json()["image1"], use_column_width=True)
        col3.image(result.json()["image2"], use_column_width=True)
        col4.image(result.json()["image3"], use_column_width=True)
        col5.image(result.json()["image4"], use_column_width=True)
    else:
        st.write("좌측에서 이미지를 넣어주세요.")



# 이후 추가될 기능

# # 옷 종류 select 기능
# category = '티셔츠'
# category = st.selectbox('옷 종류',
#                     ('티셔츠', '바지', '신발', '모자', '추가 예정'))

# st.write('You selected:', category)