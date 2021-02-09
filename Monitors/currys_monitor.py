from bs4 import BeautifulSoup
from read_csv import get_info
from send_webhook import send_webhook
from time import sleep
from global_functions import *
import os
file_name = 'currys_logs.txt'


def get_product_title(soup):
    desc_div = soup.find('span').find('div', class_='desc')

# TODO:
# get_product_title
# get_image_url
# check_availability
# get_price


def main(url):
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
            for product in products_list:
                title = get_product_title(product)
        break


if __name__ == '__main__':
    _url = 'https://www.currys.co.uk/gbuk/gaming/console-gaming/consoles/634_4783_32541_xx_xx/xx-criteria.html'
    main(_url)
