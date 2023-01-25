# import requests
# from bs4 import BeautifulSoup
from time import sleep

# urls = ['https://www.dns-shop.ru/search/?q=iphone']
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}

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
import requests

Options().add_argument('--disable-logging')

def get_info(sr): 
    sr = sr.replace(' ', '+')                           #search request
    response_ = []
    driver = webdriver.Edge('driver.exe') 
    
    driver.get('https://www.dns-shop.ru/search/?q=' + sr)                     #start dns
    products = driver.find_elements(By.CLASS_NAME, 'catalog-product')
    for product in products:
        title = product.find_element(By.CLASS_NAME,'catalog-product__name').text
        price = product.find_element(By.CLASS_NAME,'product-buy__price').text.split('\n')[0]
        rating = product.find_element(By.CLASS_NAME,'catalog-product__rating').get_attribute('data-rating')
        img = BeautifulSoup(product.find_element(By.CLASS_NAME, 'catalog-product__image-link').get_attribute('innerHTML')).find('img')['data-src']

        response_.append({'title': title, 'price': price, 'rating': rating, 'img': img, 'store':'dns'})                        #end dns
    
    
    driver.get('https://www.citilink.ru/search/?text=' + sr)
    products = BeautifulSoup(driver.page_source, 'html.parser').find_all('div', class_='ProductCardVertical')    #print(BeautifulSoup(page.text, 'html.parser'))
    for product in products:
        title = product.find('a', class_='ProductCardVertical__name').text
        price = product.find('span', class_='ProductCardVerticalPrice__price-current_current-price').text.replace(' ', '').replace('\n', '')
        try:
            rating = product.find('span', class_='ProductCardVerticalMeta__count ').text
        except Exception:
            rating = ''
        img = product.find('div', class_='ProductCardVertical__picture-hover_part')['data-src']
        response_.append({'title': title, 'price': price, 'rating': rating, 'img': img, 'store':'citilink'})

    # page = requests.get('https://shop.mts.ru/search/?TYPE=products&q=' + sr, headers=headers)


    # products = BeautifulSoup(page.text, 'html.parser').find_all('div', 'card-product-wrapper')
    # print(BeautifulSoup(page.text, 'html.parser'))
    # for product in products:
    #     if product.find('button', class_='buy-button')['style'] == 'display:none;':
    #         pass
    #     else:
    #         title = product.find('span', class_='shaved-text__original-text').text
    #         price = product.find('span', class_='product-price__current').text
    #         rating = product.find('span', class_='assessment-product__text').text
    #         img = product.find('div', class_='gallery').find('img')['src']
    #     response_.append({'title': title, 'price': price, 'rating': rating, 'img': img, 'store':'mts'})

    driver.get('https://re-store.ru/search/?q='+sr)
    producrs = []
    while True:
        try:
            print(driver.find_element(By.CLASS_NAME, 'ddl_product').get_attribute('innerHTML'))
            break

        except Exception:
            pass
    products = driver.find_elements(By.CLASS_NAME, 'ddl_product')
    print(products)
    for product in products:
        title = product.find_element(By.CLASS_NAME, 'catalog__item-title').text
        price = product.find_element(By.CLASS_NAME, 'actual-price').text
        rating = ''
        img = product.find_element(By.CLASS_NAME, 'catalog__item-img-link').find_element(By.CLASS_NAME, 'lazyload').get_attribute('src')
        response_.append({'title': title, 'price': price, 'rating': rating, 'img': img, 'store':'restore'})

    driver.quit()
    return response_

for i in get_info('iphone'):
    print(i)
#/div[1]/a/picture/img
#/html/body/div[2]/div/div[3]/div[2]/div[2]/div/div[1]/div[1]/div[1]/a