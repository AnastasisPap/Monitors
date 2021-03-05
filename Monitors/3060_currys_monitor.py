from bs4 import BeautifulSoup
from global_functions import *
from send_webhook import send_webhook
from time import sleep
file_name = '3060_currys_logs.txt'


def check_availability(soup):
    try:
        product_availability = soup.find('ul', {'data-product': 'availability'}).find_all('li')
        for li in product_availability:
            availability = li['class'][0]
            if availability == 'available':
                return True

        return False
    except:
        append_to_logs(file_name, f'Error finding availability {get_time()}\n')
        append_to_logs(file_name, soup.prettify())


def get_title(soup):
    try:
        title = soup.find('span', {'data-product': 'name'}).text
        return title
    except:
        append_to_logs(file_name, f'Error finding title {get_time()}\n')
        append_to_logs(file_name, soup.prettify())
        return 'Error finding title'


def get_product_url(soup):
    try:
        url = soup.find('a', class_='product-desc-link')['href']
        return url
    except:
        append_to_logs(file_name, f'Error finding product url {get_time()}\n')
        append_to_logs(file_name, soup.prettify())
        return 'No url'


def get_price(soup):
    try:
        price = soup.find('strong', {'data-product': 'price'}).text.replace(" ", "").replace("\n", "")
        return price
    except:
        append_to_logs(file_name, f'Error finding price {get_time()}\n')
        append_to_logs(file_name, soup.prettify())
        return 'None'


def get_image_url(soup):
    try:
        image_url = soup.find('img')["src"]
        return image_url
    except:
        append_to_logs(file_name, f'Error finding image url {get_time()}\n')
        append_to_logs(file_name, soup.prettify())
        return 'https://nelowvision.com/wp-content/uploads/2018/11/Picture-Unavailable.jpg'


def main(url):
    hasSent = False
    append_to_logs(file_name, f'Started monitor {get_time()}\n')

    while True:
        headers = {'Accept': '*/*', 'Connection': 'keep-alive',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
                   'Accept-Language': 'en-US;q=0.5,en;q=0.3', 'Cache-Control': 'max-age=0', 'DNT': '1',
                   'Pragma': 'no-cache'}
        res = get_content(url, headers, file_name, None)
        if res:
            soup = BeautifulSoup(res.content, 'html.parser')
            products = soup.find('div', {'data-component': 'product-list-view'}).find_all('article')
            for product in products:
                isAvailable = check_availability(product)
                if isAvailable:
                    title = get_title(product)
                    price = get_price(product)
                    image_url = get_image_url(product)
                    url = get_product_url(product)
                    product_id = product['id'].strip('product')
                    send_webhook(url, "Curry's: item in stock", title, image_url, price, product_id)
                sleep(0.2)
        break


if __name__ == '__main__':
    _url = 'https://www.currys.co.uk/gbuk/rtx-3060/components-upgrades/graphics-cards/324_3091_30343_xx_ba00013562-bv00314002/xx-criteria.html'
    main(_url)
