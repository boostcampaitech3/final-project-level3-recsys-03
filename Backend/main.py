from fastapi import FastAPI, File
import uvicorn
from starlette.responses import Response
from inference_backend import get_similar_fashion_model, get_category_model
import io
from PIL import Image
    
app = FastAPI()


@app.post("/")
def read_root():
	'''
	backend의 root 경로로 request가 들어올 시 dict를 return
	Parameters: None
	return : 
	dict(dtype=dict) : name과 test 이미지 경로가 들어있는 dict를 반환. 
 	({"name"(dtype=str): "Backend/img_test"(dtype=str)}
  	
   	※현재 demo test를 위해 img 파일의 형식을 img_test로 강제로 바꿔서 추가했으며 이후 이 부분은 삭제될 예정 
	'''
	return {"name": "Backend/img_test"}


@app.post("/getSimilarFashion")
def get_similar_fashion(file: bytes = File(...)):
	img = io.BytesIO(file)
	img = Image.open(img)
	img = img.convert("RGB")
	img.save('/opt/ml/musinsa_dataset/test/test_img.jpg')
	category, topk_title, topk_price, topk_item_url, topk_img_url = get_similar_fashion_model(image=file)

	return_dict = {}
	return_dict['category'] = category
	
	for i in range(5):
		return_dict['image'+str(i)] = [topk_title[i],topk_price[i],topk_item_url[i],topk_img_url[i]]
	
	return return_dict


@app.post("/getCategory")
def get_category(file: bytes = File(...)):
	category = get_category_model(file)
	return {"category" : category}


# 앞으로 기능이 추가되면 사용될 예시
# @app.get("/users/{user_id}")
# def get_user(user_id):
#     return {"user_id":user_id}

if __name__ == '__main__':
	uvicorn.run("main:app", host="0.0.0.0", port = 8000, reload=True) 