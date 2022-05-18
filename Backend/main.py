from fastapi import FastAPI
import uvicorn

    
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

# 앞으로 기능이 추가되면 사용될 예시
# @app.get("/users/{user_id}")
# def get_user(user_id):
#     return {"user_id":user_id}

if __name__ == '__main__':
	uvicorn.run("main:app", host="0.0.0.0", port = 8000, reload=True) 