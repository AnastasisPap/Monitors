from bs4 import BeautifulSoup
from product_classes import *
from time import sleep
import ast
from global_functions import *
file_name = 'gamestop_logs.txt'


def get_url(soup):
    try:
        url = soup.find('div', class_='image-container').find('a')['href']
        return 'https://www.gamestop.com' + url
    except:
        append_to_logs(file_name, f'Error finding url {get_time()}\n{str(soup)}')


def get_data(soup):
    try:
        data = soup.find('button', class_='add-to-cart')['data-gtmdata']
        data_dict = ast.literal_eval(data)
        return data_dict
    except:
        append_to_logs(file_name, f'Error getting data {get_time()}\n{str(soup)}')


def get_image_url(url, product_id):
    title = url.split('products/')[1].strip(f'/{product_id}.html')
    image_url = f'https://media.gamestop.com/i/gamestop/{product_id}/{title}?$newgrid$&fmt=webp'
    return image_url


def main(url):
    append_to_logs(file_name, f'Started monitor {get_time()}\n')
    items = Products()

    while True:
        proxies = {'https': 'http://RB4wBtGx:PSDba4RQhc127TqurOZHb2N8xBw96DYaiIekM9gxpmxz8CCm46NWNL1doQTIlqIbDxGJo-wqMTVEPmZm@ustr24.resi.ocu.privresi.com:45476'}
        proxies['https'] = get_proxy(proxies['https'])
        res = get_content(url, file_name, proxies)
        if res:
            soup = BeautifulSoup(res.content, 'html.parser')
            try:
                product_list = soup.find_all('div', class_='product-grid-tile-wrapper')

                for i, item in enumerate(product_list):
                    url = get_url(item)
                    item = Product(url, product_list[i])
                    items.add_product(item)

                for item in items.products_list:
                    data = get_data(item.code)
                    product_info = data['productInfo']
                    isAvailable = False if 'not' in product_info['availability'].lower() else True
                    if isAvailable:
                        item.set_title(product_info['name'])
                        item.set_image_url(get_image_url(url, product_info['productID']))
                        item.set_price('$'+data['price']['sellingPrice'])
                        item.set_sku(product_info['sku'])
                        item.send_webhook('GameStop')
                        item.hasSent = True
                        append_to_logs(file_name, f'Found item in stock check discord {get_time()}\n')
                        sleep(0.5)
                    else:
                        item.hasSent = False

            except:
                append_to_logs(file_name, f'Error finding products {get_time()}')
        sleep(2)


main('https://www.gamestop.com/video-games/pc-gaming/components/graphics-cards')
