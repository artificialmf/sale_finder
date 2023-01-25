from flask import Flask, render_template, url_for, request, redirect
import requests
from flask_sqlalchemy import SQLAlchemy

from bs4 import BeautifulSoup


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
import requests
from operator import itemgetter

Options().add_argument('--disable-logging')

def get_info(sr): 
    sr = sr.replace(' ', '+')                           #search request
    response_ = []
    driver = webdriver.Edge('driver.exe') 
    
    driver.get('https://www.dns-shop.ru/search/?q=' + sr)                     #start dns
    products = driver.find_elements(By.CLASS_NAME, 'catalog-product')
    for product in products:
        title = product.find_element(By.CLASS_NAME,'catalog-product__name').text
        price = int(product.find_element(By.CLASS_NAME,'product-buy__price').text.split('\n')[0].replace(' ', '').replace('₽', ''))
        rating = product.find_element(By.CLASS_NAME,'catalog-product__rating').get_attribute('data-rating')
        img = BeautifulSoup(product.find_element(By.CLASS_NAME, 'catalog-product__image-link').get_attribute('innerHTML')).find('img')['data-src']

        response_.append({'title': title, 'price': price, 'rating': rating, 'img': img, 'store':'dns'})                        #end dns
    
    
    driver.get('https://www.citilink.ru/search/?text=' + sr)
    products = BeautifulSoup(driver.page_source, 'html.parser').find_all('div', class_='ProductCardVertical')    #print(BeautifulSoup(page.text, 'html.parser'))
    for product in products:
        title = product.find('a', class_='ProductCardVertical__name').text
        price = int(product.find('span', class_='ProductCardVerticalPrice__price-current_current-price').text.replace(' ', '').replace('\n', '').replace('₽', ''))
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

    # driver.get('https://re-store.ru/search/?q='+sr)
    # producrs = []
    # while True:
    #     try:
    #         print(driver.find_element(By.CLASS_NAME, 'ddl_product').get_attribute('innerHTML'))
    #         break

    #     except Exception:
    #         pass
    # products = driver.find_elements(By.CLASS_NAME, 'ddl_product')
    # print(products)
    # for product in products:
    #     title = product.find_element(By.CLASS_NAME, 'catalog__item-title').text
    #     price = product.find_element(By.CLASS_NAME, 'actual-price').text
    #     rating = ''
    #     img = product.find_element(By.CLASS_NAME, 'catalog__item-img-link').find_element(By.CLASS_NAME, 'lazyload').get_attribute('src')
    #     response_.append({'title': title, 'price': price, 'rating': rating, 'img': img, 'store':'restore'})

    driver.quit()
    return response_
        

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
# db = SQLAlchemy(app)

# class items(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(200), nullable=False)
#     price = db.Column(db.Integer, nullable=False)
#     rating = db.Column(db.String(10), nullable=True)
#     img = db.Column(db.String(500))

#     def __repr__(self):
#         return '<product %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        search = request.form['req']
        print(search)
        products = sorted(get_info(search), key=itemgetter('price'))
        return render_template('response.html', products=products)
    else:
        return render_template('index.html')
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/response', methods=['POST', 'GET'])
def response():
    if request.method == 'POST':
        search = request.form['req']
        return redirect('/response')
    else:
        return render_template('response.html')

if __name__ == '__main__':
    app.run(debug=True)