"""
Program Details: Scrape data from a given website and store it in a database
Author: Sai Pratheek Reddy Kasarla
Database: Firebase

"""
import os
import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def scrape_website():
    #path of the current directory
    path = os.getcwd()
    
    #name of the path
    certificate_file_name = 'scraping-data-49dbc-firebase-adminsdk-9g0rw-0166949a2a.json'
    
    #complete path of the firebase crendtial certificate
    certificate_file_path = os.path.join(path, certificate_file_name)
    cred = credentials.Certificate(certificate_file_path)
    firebase_admin.initialize_app(cred)
    #creating db
    db = firestore.client()
    products_data = []
    print('Data scraping starting...')
    count = 0 #mainly used for for id
    
    # loop over the range of 1 to 50 for getting data of the products from the 50 pages
    for i in range(1, 51):
        current_url = f'https://books.toscrape.com/catalogue/page-{i}.html'
        req = requests.get(current_url)
        soup = BeautifulSoup(req.content, 'lxml')
        products = soup.find_all('li', class_ = 'col-xs-6 col-sm-4 col-md-3 col-lg-3')
        for index, product  in enumerate(products):
            product_title = product.find('h3').text
            product_price = product.find('p', class_= 'price_color').text
            product_availability = product.find('p', class_= 'instock availability').text.strip()
            product_rating = product.find('article').p['class'][1]
            product_dict = {
                'id' : str(int(count)),
                'product_title': str(product_title),
                'product_price': str(product_price[1:]),
                'product_availability': str(product_availability),
                'product_rating': str(product_rating)
            }
            products_data.append(product_dict)
            count += 1
        print(f'Page {i} scraped...')
    for data in products_data:
        doc_ref = db.collection('scraped_data').document()
        doc_ref.set(data)
    print('Data scraping completed!!')
    
if __name__ == '__main__':
    scrape_website()