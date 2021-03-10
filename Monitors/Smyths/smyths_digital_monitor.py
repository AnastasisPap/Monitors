from bs4 import BeautifulSoup
from read_csv import get_info
from send_webhook import send_webhook
from time import sleep
from global_functions import *
import os
file_name = 'smyths_digital_logs.txt'


def get_product_title(soup):
    try:
        title_div = soup.find('div', class_='detail_right margn_tp_n')
        title = title_div.find('h1', class_='margn_top_10').text
        return title
    except:
        append_to_logs(file_name, f"Error finding product title html code | {get_time()}\n")
        append_to_logs(file_name, soup.prettify())


def get_image_url(soup):
    try:
        image_src = soup.find('img', class_='responsive-image owl-lazy')['data-src']
        return image_src
    except:
        append_to_logs(file_name, f"Error finding image, script {get_time()}\n")
        append_to_logs(file_name, soup.prettify())


def check_availability(soup):
    try:
        home_delivery_in_stock = soup.find(id='hdNotAvailable')
        if home_delivery_in_stock:
            return False
        return True
    except:
        append_to_logs(file_name, f"Error finding availability, script {get_time()}\n")
        append_to_logs(file_name, soup.prettify())


def get_price(soup):
    try:
        price_div = soup.find('div', class_='price_tag')
        price = price_div.find('span', class_='notranslate').text
        return price
    except:
        append_to_logs(file_name, f'Error finding offer list | {get_time()}\n')
        append_to_logs(file_name, soup.prettify())


def main(url):
    hasSent = False

    append_to_logs(file_name, f'Started monitor {get_time()}\n')
    while True:
        headers = {
            "Accept-Language": "en-US,en;q=0.9,el;q=0.8,la;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
        }
        import requests
        res = requests.get(url, headers=headers)
        sleep(2)
        res = requests.get(url, headers=headers, cookies=res.cookies)
        print(res.content)
        res = get_content(url, headers, file_name)
        if res:

            for cookie in res.cookies:
                print(cookie)
            soup = BeautifulSoup(res.content, 'html.parser')
            isAvailable = check_availability(soup)
            if not isAvailable and hasSent:
                hasSent = False

            if isAvailable and not hasSent:
                append_to_logs(file_name, f"Found item in stock check discord {get_time()}\n")
                hasSent = True
                image_url = get_image_url(soup)
                price = get_price(soup)
                title = get_product_title(soup)
                sku = url.split('/')[-1]
                # send_webhook(url, 'Smyths Toys: item in stock', title, image_url, price, sku)

        sleep(2)


if __name__ == '__main__':
    websites = get_info()[0]
    _url = websites['smyths_digital_url']
    main(_url)
