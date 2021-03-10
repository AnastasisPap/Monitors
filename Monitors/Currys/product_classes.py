from send_webhook import send_webhook


class Product:
    def __init__(self, title, code):
        self.title = title
        self.price = ''
        self.image_url = ''
        self.url = ''
        self.availability = False
        self.product_id = ''
        self.code = code
        self.hasSent = False

    def set_id(self, product_id):
        self.product_id = product_id

    def set_image_url(self, image_url):
        self.image_url = image_url

    def set_price(self, price):
        self.price = price

    def set_url(self, url):
        self.url = url

    def send_webhook(self, store):
        if not self.hasSent:
            send_webhook(self.url, f'{store}: item in stock', self.title, self.image_url, self.price, self.product_id)


class Products:
    def __init__(self):
        self.products_list = []

    def add_product(self, item):
        flag = False
        for product in self.products_list:
            if item.title == product.title:
                flag = True

        if not flag:
            self.products_list.append(item)
