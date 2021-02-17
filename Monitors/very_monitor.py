from bs4 import BeautifulSoup
from read_csv import get_info
from send_webhook import send_webhook
from time import sleep
from global_functions import *
file_name = 'very_logs.txt'


def check_availability(products, keyword):
    for i, product in enumerate(products):
        try:
            title = product.find('span', class_='productBrandDesc').text.replace("\n", "").lower()
            if keyword in title:
                return i, True, title
        except:
            append_to_logs(file_name, f'Error finding product description {get_time()}\n')
            append_to_logs(file_name, f'{product}\n')

    return None, False, None


def get_image_url(soup):
    try:
        image_url = soup.find('img')['src']
        return image_url
    except:
        append_to_logs(file_name, f'Error finding image {get_time()}\n')
        append_to_logs(file_name, f'{soup}\n')


def get_price(soup):
    try:
        price = soup.find('dd', class_='productPrice').text.replace("\n", "")
        return price
    except:
        append_to_logs(file_name, f'Error finding price {get_time()}\n')
        append_to_logs(file_name, f'{soup}\n')


def get_link(soup):
    try:
        url = soup.find('a', class_='productMainImage')['href']
        return url
    except:
        append_to_logs(file_name, f'Error finding link {get_time()}\n')
        append_to_logs(file_name, f'{soup}\n')


def main(url, keyword):
    hasSent = False

    append_to_logs(file_name, f'Started monitor {get_time()}\n')
    while True:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15'}
        res = get_content(url, headers, file_name)
        
        if res:
            soup = BeautifulSoup(res.content, 'html.parser')
            try:
                products_list = soup.find(id='products')
                products = products_list.find_all('li', class_='product')
                idx, isAvailable, title = check_availability(products, keyword)
            
                if not isAvailable and hasSent:
                    hasSent = False

                if isAvailable and not hasSent:
                    new_soup = products[idx]
                    product_id = new_soup['id'].strip('product-prod')
                    append_to_logs(file_name, f'Found item in stock check discord {get_time()}\n')
                    hasSent = True
                    image_url = get_image_url(new_soup)
                    price = get_price(new_soup)
                    link = get_link(new_soup)
                    send_webhook(link, 'Very: item in stock', title, image_url, price, product_id)
            except:
                append_to_logs(file_name, f'Error finding products {get_time()}\n')
                append_to_logs(file_name, f'{soup}\n')
        sleep(2)


if __name__ == '__main__':
    websites = get_info()[0]
    _url = websites['very_url']
    main(_url, 'playstation')
