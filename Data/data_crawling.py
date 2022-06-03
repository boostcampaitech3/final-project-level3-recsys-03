from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
import os, time
import urllib.request

from google.oauth2 import service_account
import pandas as pd

from data_load import load_to_bigquery

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options, service=Service('/opt/ml/chromedriver'))

cd = service_account.Credentials.from_service_account_file('/opt/ml/final-project-level3-recsys-03/Data/clear-shell-351201-702c702ea7fc.json')
project_id = 'clear-shell-351201'
destination_table = 'musinsadb.articles'

def changeUrl(pagenum, category):
    url = "https://www.musinsa.com/category/" + category + "?d_cat_cd=" + category + "&brand=&rate=&page_kind=search&list_kind=small&sort=pop&sub_sort=&page=" + str(pagenum) + "&display_cnt=90&sale_goods=&group_sale=&kids=N&ex_soldout=&color=&price1=&price2=&exclusive_yn=&shoeSizeOption=&tags=&campaign_id=&timesale_yn=&q=&includeKeywords=&measure="
    return url

def get_category_items(category_list):
    
    data = list()
    
    for category in category_list:

        print(category+" crawling start...")

        url = changeUrl(1, category)
        driver.get(url)

        # make directory
        output_save_folder_path = './images/'+category+'/'
        if not os.path.exists(output_save_folder_path):
            os.makedirs(output_save_folder_path)

        for i in range(10):
            url =  changeUrl(i+1, category)
            driver.get(url)
            
            items = driver.find_elements(By.CLASS_NAME,'li_box')

            for item in items:
                try:
                    time.sleep(0.5)
                    
                    item_info = item.find_element(By.CLASS_NAME,'li_inner')
                    
                    img = item_info.find_element(By.CLASS_NAME,'list_img')
                    
                    goods = img.find_element(By.TAG_NAME,'a')
                    goods_link = goods.get_attribute('href')
                    goods_title = goods.get_attribute('title')

                    #get 500x600 image url
                    img_info = goods.find_element(By.CSS_SELECTOR,'.lazyload.lazy')
                    imgUrl = img_info.get_attribute('data-original')
                    imgUrl = imgUrl.replace('_125','_500')

                    article = item_info.find_element(By.CLASS_NAME,'article_info')
                    
                    brand = article.find_element(By.CLASS_NAME,'item_title').find_element(By.TAG_NAME,'a').text
                    price = article.find_element(By.CLASS_NAME,'price').text.split()
                    
                    data_no = item.get_attribute('data-no')
                    article_id = category + data_no

                    data.append([article_id, category, brand, goods_title, price[0], goods_link, imgUrl])
                    
                    urllib.request.urlretrieve(imgUrl, output_save_folder_path + article_id + ".jpg")
                    
                except Exception as NoSuchElementException:
                    pass

            print(f'{category} {i+1}page end....')        

    driver.close()
    print("close driver...")
    df = pd.DataFrame(data=data, columns=['article_id', 'category', 'brand', 'title', 'price', 'item_url', 'img_url'])
    return df


# ex) https://www.musinsa.com/category/003009
category_list = ["022001","022002","022003"]

result = get_category_items(category_list)
load_to_bigquery(result,'musinsadb.features')
