from bs4 import BeautifulSoup
from read_csv import get_info
from send_webhook import send_webhook
from time import sleep
from global_functions import *
import os
file_name = 'currys_logs.txt'


def get_product_title(soup):
    try:
        title_div = soup.find('div', class_='desc').find('span', {"data-product": "name"})
        return title_div.text
    except:
        append_to_logs(file_name, f'Error finding product title {get_time()}\n')
        append_to_logs(file_name, f'{soup.prettify()}')


def check_availability(titles, keyword):
    for i, title in enumerate(titles):
        if keyword in title:
            return i, True

    return None, False


def get_image_url(soup):
    try:
        image_div = soup.find('div', class_='productListImage')
        image_url = image_div.find('img')['src']
        return image_url
    except:
        append_to_logs(file_name, f'Error finding image url {get_time()}\n')
        append_to_logs(file_name, f'{soup.prettify()}')


def get_price(soup):
    try:
        price_div = soup.find('div', class_='productPrices')
        price = price_div.find('strong', class_='price').text.replace(" ", "").replace('\n', "")
        return price
    except:
        append_to_logs(file_name, f'Error finding price {get_time()}\n')
        append_to_logs(file_name, f'{soup.prettify()}')


def get_link(soup):
    try:
        link = soup.find('a')['href']
        return link
    except:
        append_to_logs(file_name, f'Error finding link {get_time()}\n')
        append_to_logs(file_name, f'{soup.prettify()}')


def main(url, keyword):
    hasSent = False
    if file_name in os.listdir():
        os.remove(file_name)

    while True:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15'}

        res = get_content(url, headers, file_name)
        if res:
            soup = BeautifulSoup(res.content, 'html.parser')
            products_list = soup.find('div', class_='col12 resultGrid').find_all('article')
            titles = []
            for product in products_list:
                title = get_product_title(product)
                titles.append(title.lower())

            idx, isAvailable = check_availability(titles, keyword)
            
            if not isAvailable and hasSent:
                hasSent = False

            if isAvailable and not hasSent:
                new_soup = products_list[idx]
                product_id = new_soup['id'].strip('product')
                title = titles[idx]
                append_to_logs(file_name, f'Found item in stock check discord {get_time()}\n')
                hasSent = True
                image_url = get_image_url(new_soup)
                price = get_price(new_soup)
                link = get_link(new_soup)
                send_webhook(link, 'Currys: item in stock', title, image_url, price, product_id) 
        
        sleep(2)


if __name__ == '__main__':
    websites = get_info()[0]
    _url = websites['currys_url']
    keyword = websites['keyword']
    main(_url, keyword)
