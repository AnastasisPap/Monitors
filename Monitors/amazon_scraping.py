import requests
from bs4 import BeautifulSoup
from read_csv import get_info
from send_webhook import send_webhook
from time import sleep
from fake_headers import Headers
from datetime import datetime
import os


def get_new_url(url):
    id = url.split('dp/')[1]
    new_url = f'https://www.amazon.co.uk/gp/aod/ajax/ref=dp_aod_afts?asin={id}&m=&pinnedofferhash'
    return new_url


# def get_price(soup):
#     try:
#         offers = soup.find_all(id='aod-offer')
#         i = 0
#         for offer in offers:
#             condition = offer.find(id='aod-offer-heading').contents[1].lower()
#             if 'used' in condition:
#                 continue
#             else:
#                 price_div = offer.find(id=f'aod-price-{i+1}')
#                 price_span = price_div.find('span', class_='a-offscreen')
#                 print(price_span.text)
#     except:
#         append_to_logs(f'Error finding offer list | {get_time()}\n')
#         append_to_logs(soup.prettify())


def get_time():
    return datetime.now().strftime("%H:%M:%S")


def append_to_logs(message):
    with open('logs.txt', 'a') as logs:
        logs.write(message)


def get_headers():
    return Headers(os="mac", headers=True).generate()


def get_content(url, headers):
    try:
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            append_to_logs(f"Error, status code: {res.status_code} | {get_time()}\n")
            print(f"Got status code: {res.status_code}")
            while res.status_code == 503:
                print("Header banned")
                get_content(url, get_headers())
        else:
            return res
    except:
        print(f"URL not found: {url}")


def get_product_title(soup):
    try:
        title = soup.find(id='aod-asin-title-text')
        return title.text.strip('\n')
    except:
        append_to_logs(f"Error finding product title html code | {get_time()}\n")
        append_to_logs(soup.prettify())


def check_availability(soup):
    new_soup = soup.find(id='aod-offer-list')
    try:
        available = new_soup.find(id='aod-total-offer-count')['value']
        if int(available) > 0:
            return True
        return False
    except:
        append_to_logs(f"Error finding availability, script {get_time()}\n")
        append_to_logs(new_soup.prettify())


def get_image_url(soup):
    try:
        url = soup.find(id='aod-asin-image-id')['src']
        return url
    except:
        append_to_logs(f"Error finding image, script {get_time()}\n")
        append_to_logs(soup.prettify())


def main(url):
    url = get_new_url(url)
    prevAvailable = True
    if "logs.txt" in os.listdir():
        os.remove("logs.txt")
    while True:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15'}
        res = get_content(url, headers)
        if res:
            soup = BeautifulSoup(res.content, 'html.parser')
            isAvailable = check_availability(soup)
            if not isAvailable:
                prevAvailable = False
            productTitle = get_product_title(soup)
            append_to_logs(f"Checking availability {get_time()}\n")
            if isAvailable and prevAvailable:
                # lowest_price = get_price(soup)
                prevAvailable = False
                append_to_logs(f"Found item in stock check discord {get_time()}\n")
                image_url = get_image_url(soup)
                send_webhook(url, 'Item in stock', productTitle, image_url)
        sleep(3)


if __name__ == '__main__':
    websites = get_info()
    main(websites[0]['url'])
