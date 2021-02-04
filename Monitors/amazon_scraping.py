import requests
from bs4 import BeautifulSoup
from read_csv import get_info

def get_price():
    websites = get_info()
    for website in websites:
        website_name = website['website']
        url = website['url']
        ids = website['id']
        classes = website['class_to_search']
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        price = 'Not available'
        if ids[0] == '0':
            for _class in classes:
                element = _class.split('/')[0]
                class_name = _class.split('/')[1]
                item = soup.find(element, class_=class_name)
                if item:
                    price = item.text
                    break
        else:
            for _id in ids:
                item = soup.find(id=_id)
                if item:
                    price = item.text
                    break
        print(f'Price: {price}, on the website {website_name}')
