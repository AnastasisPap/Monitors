from bs4 import BeautifulSoup
from time import sleep
from global_functions import *
from product_classes import *
file_name = 'very_logs.txt'


def check_availability(soup, item_id):
    try:
        curr_id = soup['data-sdg-id']
        if curr_id in item_id:
            return True
        return False
    except:
        append_to_logs(file_name, f'Error finding item id {get_time()}\n {soup}\n')
        return False


def get_ids(soup):
    ids = []
    for item in soup:
        ids.append(item['data-sdg-id'])

    return ids


def get_title_url(soup):
    try:
        details = soup.find('a', class_='productTitle')
        url = details['href']
        title = details.find('span').text.replace("\n", "")
        return title, url

    except:
        append_to_logs(file_name, f'Error finding title {get_time()}\n {soup}\n')
        return 'Error finding title'


def get_image_url(soup):
    try:
        image_url = soup.find('a', class_='productMainImage').find('img')['src']
        return image_url
    except:
        append_to_logs(file_name, f'Error finding image url {get_time()}\n {soup}\n')
        return 'https://www.metrorollerdoors.com.au/wp-content/uploads/2018/02/unavailable-image-300x225.jpg'


def get_price(soup):
    try:
        price = soup.find('a', class_='productPrice').text.replace('\n', '').replace(' ', '')
        return price
    except:
        append_to_logs(file_name, f'Error finding price {get_time()}\n {soup}')
        return 'None'


def main(url, item_id):
    append_to_logs(file_name, f'Started monitor {get_time()}\n')
    items = Products()
    while True:
        res = get_content(url, file_name, None)
        if res:
            soup = BeautifulSoup(res.content, 'html.parser')
            try:
                products_list = soup.find('ul', class_='productList').find_all('li', class_='product')
                ids = get_ids(products_list)

                for i, prod_id in enumerate(ids):
                    item = Product(prod_id, products_list[i])
                    items.add_product(item)

                for item in items.products_list:
                    isAvailable = check_availability(item.code, item_id)

                    if isAvailable:
                        new_soup = item.code
                        title, url = get_title_url(new_soup)
                        item.set_title(title)
                        item.set_image_url(get_image_url(new_soup))
                        item.set_price(get_price(new_soup))
                        item.set_url(url)
                        item.set_sku(item_id)
                        item.send_webhook('Very UK')
                        item.hasSent = True
                        append_to_logs(file_name, f'Found item in stock check discord {get_time()}\n')
                        sleep(0.5)
                    else:
                        item.hasSent = False
            except:
                append_to_logs(file_name, f'Error finding products {get_time()}\n')

        sleep(2)


if __name__ == '__main__':
    main('https://www.very.co.uk/e/q/playstation-5-console.end?_requestid=108264', '1600104783')
