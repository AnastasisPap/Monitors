from bs4 import BeautifulSoup
from product_classes import *
from time import sleep
from global_functions import *
file_name = 'currys_logs.txt'


def get_product_title(soup):
    try:
        title_div = soup.find('div', class_='desc').find('span', {"data-product": "name"})
        return title_div.text
    except:
        append_to_logs(file_name, f'Error finding product title {get_time()}\n')
        append_to_logs(file_name, f'{soup.prettify()}')


def check_availability(title, keyword, soup):
    if keyword in title:
        try:
            lis = soup.find('ul', {'data-product': 'availability'}).find_all('li')
            for li in lis:
                if li["class"][0] == "available":
                    return True
        except:
            append_to_logs(file_name, f'Error finding ul {get_time()}\n')
            append_to_logs(file_name, f'{soup}\n')

    return False


def get_image_url(soup):
    try:
        image_div = soup.find('div', class_='productListImage')
        image_url = image_div.find('img')['src']
        return image_url
    except:
        append_to_logs(file_name, f'Error finding image url {get_time()}\n')
        append_to_logs(file_name, f'{soup.prettify()}')


def get_price(soup):
    try:
        price_div = soup.find('div', class_='productPrices')
        price = price_div.find('strong', class_='price').text.replace(" ", "").replace('\n', "")
        return price
    except:
        append_to_logs(file_name, f'Error finding price {get_time()}\n')
        append_to_logs(file_name, f'{soup.prettify()}')


def get_link(soup):
    try:
        link = soup.find('a')['href']
        return link
    except:
        append_to_logs(file_name, f'Error finding link {get_time()}\n')
        append_to_logs(file_name, f'{soup.prettify()}')


def main(url, keyword):
    append_to_logs(file_name, f'Started monitor {get_time()}\n')
    items = Products()
    while True:
        res = get_content(url, file_name, None)
        if res:
            soup = BeautifulSoup(res.content, 'html.parser')
            
            products_list = soup.find('div', class_='col12 resultGrid').find_all('article')
            titles = []
            for product in products_list:
                title = get_product_title(product)
                titles.append(title.lower())

            for i, title in enumerate(titles):
                item = Product(title, products_list[i])
                items.add_product(item)

            for item in items.products_list:
                isAvailable = check_availability(item.title, keyword, item.code)
                if isAvailable:
                    new_soup = item.code
                    item.set_id(new_soup['id'].strip('product'))
                    item.set_image_url(get_image_url(new_soup))
                    item.set_price(get_price(new_soup))
                    item.set_url(get_link(new_soup))
                    item.send_webhook('Currys')
                    item.hasSent = True
                    append_to_logs(file_name, f'Found item in stock check discord {get_time()}\n')
                    sleep(0.2)
                else:
                    item.hasSent = False
        sleep(2)