from read_csv import get_info
from send_webhook import send_webhook
from time import sleep
import requests
import json
file_name = 'target_logs.txt'


def check_availability(product):
    availability = product["availability_status"]
    if availability == 'OUT_OF_STOCK':
        return False
    return True


def main(product_id):
    s = requests.get("https://www.target.com/")
    key = s.cookies['visitorId']
    url = f'https://redsky.target.com/v2/plp/collection/{product_id}?key={key}&pricing_store_id=2776'
    res = requests.get(url).json()
    product = res["search_response"]["items"]["Item"][0]
    isAvailable = check_availability(product)
    print(isAvailable)


if __name__ == '__main__':
    main(81114595)

    store_id = 1865
