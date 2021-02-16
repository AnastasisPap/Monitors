from read_csv import get_info
from send_webhook import send_webhook
from time import sleep
import requests
import json
from global_functions import *
file_name = 'target_logs.txt'


def get_title(product):
    return product["title"]


def check_availability(product):
    availability = product["availability_status"]
    if availability == 'OUT_OF_STOCK':
        return False
    return True


def get_price(product):
    price = product["price"]["formatted_current_price"]
    return price


def get_image(product):
    images = product["images"][0]
    base_url = images["base_url"]
    primary = images["primary"]
    return base_url + primary


def get_url(product):
    return "https://www.target.com" + product["url"]


def main(product_id):
    hasSent = False
    append_to_logs(file_name, f"Started monitor {get_time()}\n")
    while True:
        s = requests.get("https://www.target.com/")
        key = s.cookies['visitorId']
        url = f'https://redsky.target.com/v2/plp/collection/{product_id}?key={key}&pricing_store_id=2776'
        res = requests.get(url).json()
        product = res["search_response"]["items"]["Item"][0]
        isAvailable = check_availability(product)

        if not isAvailable and hasSent:
            hasSent = False

        if isAvailable and not hasSent:
            append_to_logs(file_name, 'Found item in stock {get_time()}\n')
            hasSent = True
            title = get_title(product)
            price = get_price(product)
            image_url = get_image(product)
            url = get_url(product)
            send_webhook(url, "Target: item in stock", title, image_url, price, product_id)

        sleep(2)


if __name__ == '__main__':
    main(81114474)
    
