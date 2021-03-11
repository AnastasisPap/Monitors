from bs4 import BeautifulSoup
from product_classes import *
from time import sleep
from global_functions import *
file_name = 'ebuyer_logs.txt'


def get_price(soup):
    try:
        price = soup.find('div', class_='grid-item__price').find('p', class_='price').text.replace('\n', '').replace(" ", "").strip('inc.vat')
        return price
    except:
        append_to_logs(file_name, f'Error finding price {get_time()}\n{soup.prettify()}\n')
        return 'None'


def get_urls(soup):
    try:
        details = soup.find('div', class_='grid-item__img')
        url = 'https://www.ebuyer.com' + details.find('a')['href']
        image_url = details.find('img')["src"]
        return url, image_url
    except:
        append_to_logs(file_name, f'Error finding image url {get_time()}\n{soup.prettify()}\n')
        return 'https://www.ebuyer.com/', 'https://www.metrorollerdoors.com.au/wp-content/uploads/2018/02/unavailable-image-300x225.jpg'


def get_title(soup):
    try:
        title = soup.find('h3', class_='grid-item__title').text
        return title
    except:
        append_to_logs(file_name, f'Error finding title {get_time()}\n{soup}\n')
        return 'Error finding title'


def get_ids(products):
    ids = []
    for product in products:
        ids.append(product['data-product-id'])

    return ids


def check_availability(soup):
    try:
        coming_soon = soup.find('p', class_='grid-item__coming-soon').text

        if "oming" in coming_soon:
            return False
        return True
    except:
        return True


def main(url):
    append_to_logs(file_name, f'Started monitor {get_time()}\n')
    items = Products()
    print(f'Monitor with url {url} has started - {get_time()}')
    while True:
        res = get_content(url, file_name, None)
        if res:
            soup = BeautifulSoup(res.content, 'html.parser')
            try:
                products_list = soup.find_all('div', class_='grid-item js-listing-product')
                ids = get_ids(products_list)

                for i, prod_id in enumerate(ids):
                    item = Product(prod_id, products_list[i])
                    items.add_product(item)

                for item in items.products_list:
                    isAvailable = check_availability(item.code)

                    if isAvailable:
                        new_soup = item.code
                        item.set_title(get_title(new_soup))
                        url, image_url = get_urls(new_soup)
                        item.set_image_url(image_url)
                        item.set_price(get_price(new_soup))
                        item.set_url(url)
                        item.set_sku(item.product_id)
                        item.send_webhook('Ebuyer')
                        item.hasSent = True
                        append_to_logs(file_name, f'Found item in stock check discord {get_time()}\n')
                        sleep(0.5)
                    else:
                        item.hasSent = False
            except:
                append_to_logs(file_name, f'Error getting products {get_time()}\n')

        sleep(2)
