# import requests
# from bs4 import BeautifulSoup

# urls = ['https://www.dns-shop.ru/search/?q=iphone']
# headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}

# def get_info(searchreq):
#     response = []
#     page = requests.get(searchreq, headers=headers)
#     print(page.status_code)
#     soup = BeautifulSoup(page.text, 'html.parser')
#     print(soup)
#     posts = soup.find_all('div', class_='catalog-product')
#     for post in posts:
#         title = post.find('a', class_='catalog-product__name').get_text()
#         price = post.find('div', class_='product-buy__price').get_text()
#         rating = post.find('a', class_='catalog-product__rating')['data-rating']
#         img = post.find('img')['src']
#         response.append({'title': title, 'price': price, 'rating': rating, 'img': img, 'store':'dns'})
#     return response

# print(get_info(urls[0]))

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup

Options().add_argument('log-level=3')

def get_info(sr):                            #search request
    response_ = []
    driver = webdriver.Edge('driver.exe') 
    driver.get('https://www.dns-shop.ru/search/?q=' + sr)
    products = driver.find_elements(By.CLASS_NAME, 'catalog-product')
    for product in products:
        title = product.find_element(By.CLASS_NAME,'catalog-product__name').text
        price = product.find_element(By.CLASS_NAME,'product-buy__price').text.split('\n')[0]
        rating = product.find_element(By.CLASS_NAME,'catalog-product__rating').get_attribute('data-rating')
        img = product.find_element(By.CLASS_NAME, 'catalog-product__image-link').get_attribute('innerHTML')
        img = BeautifulSoup(product.find_element(By.CLASS_NAME, 'catalog-product__image-link').get_attribute('innerHTML')).find('img')['data-src']

        response_.append({'title': title, 'price': price, 'rating': rating, 'img': img, 'store':'dns'})
    
    
    driver.get('https://www.citilink.ru/search/?text=' + sr)
    
    return response_

print(get_info('iphone'))
#/div[1]/a/picture/img
#/html/body/div[2]/div/div[3]/div[2]/div[2]/div/div[1]/div[1]/div[1]/a