import requests
from bs4 import BeautifulSoup
from read_csv import get_info
from send_webhook import send_webhook
from time import sleep
from fake_headers import Headers
from datetime import datetime
import os


def get_new_url(url):
    sku = url.split('dp/')[1]
    region = url.split('amazon.')[1].split('/')[0]
    new_url = f'https://www.amazon.{region}/gp/aod/ajax/ref=dp_aod_afts?asin={sku}&m=&pinnedofferhash'
    return new_url, sku


def get_price(soup):
    try:
        offer_list = soup.find_all('div', class_='a-section a-spacing-medium a-spacing-top-base a-padding-none aod-information-block aod-clear-float')
        for i, offer in enumerate(offer_list):
            condition_div = offer.find(id='aod-offer-heading').text.lower()
            if 'used' not in condition_div:
                price = soup.find(id=f'aod-price-{i+1}').find('span', class_='a-offscreen').text
                if '£' in price or '$' in price:
                    float_price = float(price[1:])
                elif '€' in price:
                    float_price = float(price.split(',')[0])

                return price, float_price
            continue
        return 10**10, 10**10
    except:
        append_to_logs(f'Error finding offer list | {get_time()}\n')
        append_to_logs(soup.prettify())


def get_time():
    return datetime.now().strftime("%H:%M:%S")


def append_to_logs(message):
    with open('logs.txt', 'a') as logs:
        logs.write(message)


def get_content(url, headers):
    try:
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            append_to_logs(f"Error, status code: {res.status_code} | {get_time()}\n")
            print(f"Got status code: {res.status_code}")
            while res.status_code == 503:
                append_to_logs("Header banned")
                new_header = Headers(os='mac', headers=True).generate()
                get_content(url, new_header)
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


def main(url, retail):
    new_url, sku = get_new_url(url)
    hasSent = False
    if "logs.txt" in os.listdir():
        os.remove("logs.txt")
    while True:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15'}
        res = get_content(new_url, headers)
        if res:
            soup = BeautifulSoup(res.content, 'html.parser')
            isAvailable = check_availability(soup)
            append_to_logs(f"Checking availability {get_time()}\n")
            if not isAvailable and hasSent:
                hasSent = False

            if isAvailable and not hasSent:
                append_to_logs("Found item in stock")
                productTitle = get_product_title(soup)
                lowest_price, float_price = get_price(soup)
                if float_price < retail:
                    hasSent = True
                    image_url = get_image_url(soup)
                    append_to_logs(f"Found item in stock check discord {get_time()}\n")
                    send_webhook(url, 'Item in stock', productTitle, image_url, lowest_price, sku)
        sleep(3)


if __name__ == '__main__':
    websites = get_info()
    main(websites[0]['url'], int(websites[0]['retail']))
