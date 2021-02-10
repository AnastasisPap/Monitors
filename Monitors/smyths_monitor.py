from bs4 import BeautifulSoup
from read_csv import get_info
from send_webhook import send_webhook
from time import sleep
from global_functions import *
import os
file_name = 'smyths_logs.txt'


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
        append_to_logs(file_name, new_soup.prettify())


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
    if file_name in os.listdir():
        os.remove(file_name)

    while True:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15'}
        res = get_content(url, headers, file_name)
        if res:
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
                send_webhook(url, 'Smyths Toys: item in stock', title, image_url, price, sku)

        sleep(2)


if __name__ == '__main__':
    # websites = get_info()
    # main(websites[0]['url'])
    main('https://www.smythstoys.com/uk/en-gb/video-games-and-tablets/playstation-5/playstation-5-games/sackboy-a-big-adventure-ps5/p/191447')
