from time import sleep
from bs4 import BeautifulSoup
from send_webhook import send_webhook
from global_functions import *
file_name = 'amazon_logs.txt'


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
        append_to_logs(file_name, f'Error finding offer list | {get_time()}\n')
        append_to_logs(file_name, soup.prettify())


def get_product_title(soup):
    try:
        title = soup.find(id='aod-asin-title-text')
        return title.text.strip('\n')
    except:
        append_to_logs(file_name, f"Error finding product title html code | {get_time()}\n")
        append_to_logs(file_name, soup.prettify())


def check_availability(soup):
    new_soup = soup.find(id='aod-offer-list')
    try:
        available = new_soup.find(id='aod-total-offer-count')['value']
        if int(available) > 0:
            return True
        return False
    except:
        append_to_logs(file_name, f"Error finding availability, script {get_time()}\n")
        append_to_logs(file_name, new_soup.prettify())


def get_image_url(soup):
    try:
        url = soup.find(id='aod-asin-image-id')['src']
        return url
    except:
        append_to_logs(file_name, f"Error finding image, script {get_time()}\n")
        append_to_logs(file_name, soup.prettify())


def main(url, retail):
    new_url, sku = get_new_url(url)
    hasSent = False
    append_to_logs(file_name, f'Monitor started {get_time()}\n')

    while True:
        res = get_content(new_url, file_name, None)
        if res:
            soup = BeautifulSoup(res.content, 'html.parser')
            isAvailable = check_availability(soup)
            if not isAvailable and hasSent:
                hasSent = False

            if isAvailable and not hasSent:
                append_to_logs(file_name, "Found item in stock")
                productTitle = get_product_title(soup)
                lowest_price, float_price = get_price(soup)
                if float_price < retail:
                    hasSent = True
                    image_url = get_image_url(soup)
                    append_to_logs(file_name, f"Found item in stock check discord {get_time()}\n")
                    send_webhook(url, 'Amazon: item in stock', productTitle, image_url, lowest_price, sku)
        sleep(2)
