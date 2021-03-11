from bs4 import BeautifulSoup
from time import sleep
from global_functions import *
from product_classes import *
file_name = 'new_egg_logs.txt'


def check_availability(product):
    try:
        availability = product.find('p', class_='item-promo').text
        if availability == 'OUT OF STOCK':
            return False
    except:
        return True


def get_title(product):
    try:
        title = product.find('a', class_='item-title')
        url = title['href']
        title = title.text
        return title, url
    except:
        append_to_logs(file_name, f'Error finding title {get_time()}\n')
        append_to_logs(file_name, f'{product.prettify()}')
        return 'Error getting title'


def get_price(product):
    try:
        price = product.find('li', class_='price-current').text.split('.')[0]
        return price
    except:
        append_to_logs(file_name, f'Error finding price {get_time()}\n')
        append_to_logs(file_name, f'{product.prettify()}\n')
        return 'Error finding price'


def get_image_url(product):
    try:
        container = product.find('div', class_='item-container').find('img')['src']
        return container
    except:
        append_to_logs(file_name, f'Error finding image url {get_time()}\n')
        append_to_logs(file_name, f'{product.prettify()}\n')
        return 'https://www.metrorollerdoors.com.au/wp-content/uploads/2018/02/unavailable-image-300x225.jpg'


def has_items(soup):
    try:
        res = soup.find('p', class_='result-message-title').text
        if 'found 0' in res:
            return False
    except:
        return True


def get_sku(soup):
    try:
        item_features = soup.find('ul', class_='item-features').find_all('li')
        sku = item_features[-2].text.strip("Item #:")
        return sku
    except:
        append_to_logs(file_name, f'Error finding sku {get_time()}\n{soup.prettify()}\n')
        return 'None'


def get_ids(soup):
    ids = []

    for product in soup:
        ids.append(product['id'])
    return ids


def main(url):
    append_to_logs(file_name, f'Started monitor {get_time()}\n')
    items = Products()
    while True:
        res = get_content(url, file_name, None)
        if res:
            soup = BeautifulSoup(res.content, 'html.parser')
            products_res = has_items(soup)
            if products_res:
                try:
                    products_list = soup.find_all('div', class_='item-cell')
                    products_list = [product for product in products_list if product.has_attr('id')]
                    ids = get_ids(products_list)

                    for i, prod_id in enumerate(ids):
                        item = Product(prod_id, products_list[i])
                        items.add_product(item)

                    for item in items.products_list:
                        isAvailable = check_availability(item.code)
                        isAvailable = True
                        if isAvailable:
                            new_soup = item.code
                            title, url = get_title(new_soup)
                            item.set_title(title)
                            item.set_image_url(get_image_url(new_soup))
                            item.set_price(get_price(new_soup))
                            item.set_url(url)
                            item.set_sku(get_sku(new_soup))
                            item.send_webhook('New Egg')
                            item.hasSent = True
                            append_to_logs(file_name, f'Found item in stock, check discord {get_time()}\n')
                            sleep(0.5)
                        else:
                            item.hasSent = False

                        break

                except:
                    append_to_logs(file_name, f'Error finding item cells {get_time()}\n{soup}')
        sleep(2)


main('https://www.newegg.com/p/pl?N=100007709%20601357282&PageSize=96')
