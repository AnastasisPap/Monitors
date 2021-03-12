from send_webhook import send_webhook


class Product:
    def __init__(self, link, code):
        self.title = ''
        self.price = ''
        self.image_url = ''
        self.url = link
        self.availability = False
        self.code = code
        self.hasSent = False
        self.sku = ''

    def set_title(self, title):
        self.title = title

    def set_image_url(self, image_url):
        self.image_url = image_url

    def set_price(self, price):
        self.price = price

    def set_sku(self, sku):
        self.sku = sku

    def send_webhook(self, store):
        if not self.hasSent:
            send_webhook(self.url, f'{store}: item in stock', self.title, self.image_url, self.price, self.sku)


class Products:
    def __init__(self):
        self.products_list = []

    def add_product(self, item):
        flag = False
        for product in self.products_list:
            if item.url == product.url:
                flag = True

        if not flag:
            self.products_list.append(item)
