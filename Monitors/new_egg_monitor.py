from bs4 import BeautifulSoup
from read_csv import get_info
from send_webhook import send_webhook
from time import sleep
from global_functions import *
file_name = 'new_egg_logs.txt'

# get_image_url
# get_url


def check_availability(product):
    try:
        availability = product.find('p', class_='item-promo').text
        if availability == 'OUT OF STOCK':
            return False
    except:
        return True


def get_title(product):
    try:
        title = product.find('a', class_='item-title').text
        return title
    except:
        append_to_logs(file_name, f'Error finding title {get_time()}\n')
        append_to_logs(file_name, f'{product.prettify()}')


def get_price(product):
    try:
        price = product.find('li', class_='price-current').text.split('.')[0]
        return price
    except:
        append_to_logs(file_name, f'Error finding price {get_time()}\n')
        append_to_logs(file_name, f'{product.prettify()}\n')


def get_image_url(product):
    try:
        container = product.find('div', class_='item-container').find('img')['src']
        return container
    except:
        append_to_logs(file_name, f'Error finding image url {get_time()}\n')
        append_to_logs(file_name, f'{product.prettify()}\n')


def get_id(product):
    try:
        item_features = product.find('ul', class_='item-features').find_all('li')
        product_id = item_features[-2].text.strip("Item #: ")
        return product_id
    except:
        append_to_logs(file_name, f'Error finding id {get_time()}\n')
        append_to_logs(file_name, f'{product.prettify()}\n')


def main(url):
    append_to_logs(file_name, f'Started monitor {get_time()}\n')
    while True:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15'}
        res = get_content(url, headers, file_name)
        if res:
            soup = BeautifulSoup(res.content, 'html.parser')
            try:
                products = soup.find_all('div', class_='item-cell')
                products = [product for product in products if product.has_attr('id')]
                for product in products:
                    isAvailable = check_availability(product)
                    hasSent = False
                    if not isAvailable and hasSent:
                        hasSent = False

                    if isAvailable and not hasSent:
                        title = get_title(product)
                        price = get_price(product)
                        image_url = get_image_url(product)
                        product_id = get_id(product)
                        url = 'https://www.newegg.com/p/' + product_id
                        hasSent = True
                        append_to_logs(file_name, f'Found item in stock {get_time()}\n')
                        send_webhook(url, 'NewEgg: item in stock', title, image_url, price, product_id)
                        sleep(0.5)

            except:
                append_to_logs(file_name, f'Error finding products list {get_time()}\n')
                append_to_logs(file_name, f'{soup.prettify()}')
        sleep(2)


if __name__ == '__main__':
    # _url = 'https://www.newegg.com/p/pl?d=rtx+3090&N=100007709%20601357282&isdeptsrh=1'
    _url = 'https://www.newegg.com/p/pl?d=rtx&N=50001402&LeftPriceRange=400+2500'
    main(_url)
