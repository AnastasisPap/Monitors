from send_webhook import send_webhook
from time import sleep
import requests
import json
from global_functions import *
file_name = 'best_buy_logs.txt'


def check_availability(product):
    state = product["buttonState"]["buttonState"]
    if state == "SOLD_OUT" or state == 'COMING_SOON':
        return False
    return True


def get_price(product):
    price = product["price"]["currentPrice"]
    return "$" + str(price)


def get_title(product):
    title = product["names"]["short"]
    return title


def get_url(product):
    base_url = 'https://www.bestbuy.com/'
    url = product["url"]
    return base_url + url


def get_image_url(product_id):
    category_id = str(product_id)[:4]
    url = f'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/{category_id}/{product_id}_sd.jpg;maxHeight=640;maxWidth=550'
    return url


def main(product_id):
    hasSent = False
    append_to_logs(file_name, f'Started monitor {get_time()}\n')
    while True:
        headers = {'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626 Safari/537.36 OPR/56.0.3051.36', 'Accept-Language': 'en-US;q=0.5,en;q=0.3', 'Upgrade-Insecure-Requests': '1', 'Referer': 'https://google.com'}

        s = requests.get(f'https://www.bestbuy.com/api/3.0/priceBlocks?skus={product_id}', headers=headers).json()
        product = s[0]['sku']
        isAvailable = check_availability(product)
        if not isAvailable and hasSent:
            hasSent = False

        if isAvailable and not hasSent:
            append_to_logs(file_name, f"Found item in stock {get_time()}\n")
            hasSent = True
            price = get_price(product)
            title = get_title(product)
            url = get_url(product)
            image_url = get_image_url(product_id)
            send_webhook(url, "Best buy: item in stock", title, image_url, price, product_id)

        sleep(2)


if __name__ == '__main__':
    main(6439402)
