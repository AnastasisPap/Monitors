from bs4 import BeautifulSoup
from read_csv import get_info
from send_webhook import send_webhook
from time import sleep
from global_functions import *
import os
file_name = 'argos_digital_logs.txt'


def get_image_url(soup):
    try:
        image_div = soup.find('div', {'class': 'MediaGallerystyles__ImageWrapper-sc-1jwueuh-2 eDqOMU'})
        image_url = image_div.find('source')['srcset']
        return 'https:' + image_url
    except:
        append_to_logs(file_name, f'Error finding image url {get_time()}\n')
        append_to_logs(file_name, f'{soup.prettify()}')


def check_availability(soup):
    sorry_text = soup.find('div', class_='promo-text')
    if sorry_text:
        return False
    return True


def get_product_title(soup):
    try:
        title = soup.find('span', {'data-test': 'product-title'}).text
        return title
    except:
        append_to_logs(file_name, f'Error finding product title {get_time()}\n')
        append_to_logs(file_name, f'{soup.prettify()}')


def get_price(soup):
    try:
        price_div = soup.find('li', {'data-test': 'product-price-primary'})
        return price_div.find('h2').text
    except:
        append_to_logs(file_name, f'Error finding price {get_time()}\n')
        append_to_logs(file_name, f'{soup.prettify()}')


def main(url):
    hasSent = False
    if file_name in os.listdir():
        os.remove(file_name)
    append_to_logs(file_name, f'Started monitor {get_time()}\n')

    while True:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15'}

        res = get_content(url, headers, file_name)
        if res:
            soup = BeautifulSoup(res.content, 'html.parser')
            isAvailable = check_availability(soup)
            if not isAvailable and hasSent:
                hasSent = True

            if isAvailable and not hasSent:
                hasSent = True
                title = get_product_title(soup)
                price = get_price(soup)
                image_url = get_image_url(soup)
                id = url.split('/')[-1]
                send_webhook(url, 'Argos: item in stock', title, image_url, price, id)

        sleep(2)


if __name__ == '__main__':
    websites = get_info()[0]
    _url = websites['argos_digital_url']
    main(_url)
