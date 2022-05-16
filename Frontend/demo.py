import pandas as pd
import numpy as np
import streamlit as st
import requests
from streamlit_cropper import st_cropper
from PIL import Image
from requests_toolbelt.multipart.encoder import MultipartEncoder
import io
import time

backend = "http://localhost:8000/"

def getData():
    return requests.post(backend, files=files)


def process(image, server_url: str):
    
    m = MultipartEncoder(fields={"file": ("filename", image, "image/jpeg")})

    r = requests.post(
        server_url, data=m, headers={"Content-Type": m.content_type}, timeout=8000
    )

    return r

st.title('비슷한 옷을 추천해줘')

st.set_option('deprecation.showfileUploaderEncoding', False)

st.header("사진 업로드")
img_file = st.sidebar.file_uploader(label='사진 업로드', type=['png', 'jpg'])
box_color = st.sidebar.color_picker(label="테두리 색상", value='#000000')
aspect_ratio = None

if img_file:
    img = Image.open(img_file)
    # Get a cropped image from the frontend
    cropped_img = st_cropper(img, realtime_update=True, box_color=box_color,
                                aspect_ratio=aspect_ratio)
    
    # Manipulate cropped image at will
    st.write("업로드 될 사진")
    image = cropped_img.thumbnail((500,500))
    st.image(cropped_img)



if st.button("업로드 완료"):
    if cropped_img :
        files = {"file": np.array(cropped_img)}
        try:
            result = getData() 
        except:
            time.sleep(2)
            result = getData()
        img_path = result.json()
        print(img_path)
        image = Image.open(img_path.get("name"))
        st.image(image, width=500)
    else:
        st.write("좌측에서 이미지를 넣어주세요.")

st.write("무언가가 진행될 예정")

option = st.selectbox('옷 종류',
                    ('티셔츠', '바지', '신발', '모자', '추가 예정'))

st.write('You selected:', option)
