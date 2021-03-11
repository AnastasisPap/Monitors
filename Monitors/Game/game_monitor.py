from bs4 import BeautifulSoup
from read_csv import get_info
from send_webhook import send_webhook
from time import sleep
from global_functions import *
import os
file_name = 'game_logs.txt'


def get_html_info(soup):
    prices = []
    links = []
    titles = []
    image_urls = []
    ids = []
    for product in soup:
        price = product.find('div', class_='priceContainer').find('span', class_="value")
        if price is None:
            continue

        prices.append(price.text)
        product_header = product.find('div', class_='productHeader')
        desc = product_header.find('h2').find('a')
        links.append(desc['href'])
        titles.append(desc.text)
        image_urls.append('https://' + product_header.find('img')['data-src'][2:])
        ids.append(product_header["data-sku"])

    return prices, links, titles, image_urls, ids


def check_availability(url):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15'}
    res = get_content(url, headers, file_name)
    if res:
        append_to_logs(file_name, f'URL is up! {get_time()}\n')
        return True, res
    return False, None


def main(url):
    hasSent = False
    hasSentURL = False
    append_to_logs(file_name, f'Monitor started with url {url} - {get_time()}\n')

    while True:
        isAvailable, res = check_availability(url)
        if not isAvailable and hasSent:
            hasSent = False
        if isAvailable and not hasSentURL:
            send_webhook(url, 'URL is working', 'URL returned a valid status code', 'https://m.media-amazon.com/images/M/MV5BNjRlYjgwMWMtNDFmMy00OWQ0LWFhMTMtNWE3MTU4ZjQ3MjgyXkEyXkFqcGdeQXVyNzU1NzE3NTg@._V1_CR0,45,480,270_AL_UX477_CR0,0,477,268_AL_.jpg', 0, 0)
            hasSentURL = True

        if isAvailable and not hasSent:
            soup = BeautifulSoup(res.content, 'html.parser')
            append_to_logs(file_name, 'Found item in stock')
            products = soup.find(id='productContainer').find_all('article')
            hasSent = True
            prices, links, titles, image_urls, ids = get_html_info(products)
            for i in range(len(prices)):
                send_webhook(links[i], 'Game: item in stock', titles[i], image_urls[i], prices[i], ids[i])
                sleep(0.5)

        sleep(2)
