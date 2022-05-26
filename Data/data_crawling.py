from selenium import webdriver
import os, time
import urllib.request
import pandas as pd

def changeUrl(pagenum, category):
    url = "https://www.musinsa.com/category/" + category + "?d_cat_cd=" + category + "&brand=&rate=&page_kind=search&list_kind=small&sort=pop&sub_sort=&page=" + str(pagenum) + "&display_cnt=90&sale_goods=&group_sale=&kids=N&ex_soldout=&color=&price1=&price2=&exclusive_yn=&shoeSizeOption=&tags=&campaign_id=&timesale_yn=&q=&includeKeywords=&measure="
    return url

# Save crawling data to list
result = list()

driver = webdriver.Chrome('chromedriver.exe 절대 경로')

# ex) https://www.musinsa.com/category/003009
category_list = ["022001","022002","022003"]

for category in category_list:
    url = changeUrl(1, category)
    driver.get(url)

    # make directory
    output_save_folder_path = './images/'+category+'/'

    if not os.path.exists(output_save_folder_path):
        os.makedirs(output_save_folder_path)

    for i in range(10):
        url =  changeUrl(i+1, category)
        driver.get(url)
        
        items = driver.find_elements_by_class_name('li_box')

        for item in items:
            try:
                time.sleep(0.5)
                img = item.find_element_by_class_name('lazyload.lazy')
                imgUrl = img.get_attribute('data-original')
                data_no = item.get_attribute('data-no')
                article_id = category + data_no
                img_info = item.find_element_by_class_name('img-block')
                data_href = img_info.get_attribute('href')
                title = img_info.get_attribute('title')
                article_info = item.find_element_by_class_name('article_info')
                brand = article_info.find_element_by_class_name('item_title').text
                price = article_info.find_element_by_class_name('price').text.split()
                
                result.append([article_id, category, brand, title, price[0], data_href, imgUrl])
                
                urllib.request.urlretrieve(imgUrl, output_save_folder_path + category + data_no + ".jpg")
                
            except Exception as e:
                print(e)
                pass

driver.close()

# change list to dataframe
data = pd.DataFrame(result)
# Change column name
data.columns = ['article_id', 'category', 'brand', 'title', 'price', 'item_url', 'img_url']
# Save dataframe to csv
data.to_csv('data.csv')
print("save crawling data to csv")