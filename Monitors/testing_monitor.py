from bs4 import BeautifulSoup
from read_csv import get_info
from send_webhook import send_webhook
from time import sleep
from global_functions import *
import os
file_name = 'testing_logs.txt'


def get_title(soup):
    title = soup.find('h3', {'data-hook': 'product-item-name'}).text
    return title


def isAvailable(products, keyword):
    for i, product in enumerate(products):
        title = get_title(product)
        if keyword in title.lower():
            return i, True
    return None, False


def main(url, keyword):
    append_to_logs(file_name, f'Monitor started {get_time()}\n')
    hasSent = False
    while True:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15'}
        res = get_content(url, headers, file_name)
        soup = BeautifulSoup(res.content, 'html.parser')
        products = soup.find_all('li', {'data-hook': 'product-list-grid-item'})
        idx, isAv = isAvailable(products, keyword)

        if not isAv and hasSent:
            hasSent = False

        if isAv and not hasSent:
            print('ok')
            title = get_title(products[idx])
            send_webhook(url, 'Item in stock', title, 'https://m.media-amazon.com/images/M/MV5BNjRlYjgwMWMtNDFmMy00OWQ0LWFhMTMtNWE3MTU4ZjQ3MjgyXkEyXkFqcGdeQXVyNzU1NzE3NTg@._V1_CR0,45,480,270_AL_UX477_CR0,0,477,268_AL_.jpg', 100, 0)
            hasSent = True

        sleep(0.5)


if __name__ == '__main__':
    main('https://anaspap15.wixsite.com/website/shop', 'playstation 5')
