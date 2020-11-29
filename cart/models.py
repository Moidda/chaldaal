from django.db import models
from django.db import connection

cursor = connection.cursor()


class Cart:
    products = {}
    rating = {}
    total_cost = 0

    def add_product(self, product_id):
        if product_id in self.products:
            self.products[product_id] += 1
        else:
            self.products[product_id] = 1
            self.rating[product_id] = 0
        self.total_cost += cursor.callfunc('GET_PRODUCT_PRICE', int, [product_id])

    def remove_product(self, product_id):
        if product_id not in self.products:
            return
        if self.products[product_id] > 0:
            self.total_cost -= cursor.callfunc('GET_PRODUCT_PRICE', int, [product_id])
        self.products[product_id] -= 1
        self.products[product_id] = max(self.products[product_id], 0)

    def erase_product(self, product_id):
        if product_id not in self.products:
            return
        self.total_cost -= self.products[product_id]*cursor.callfunc('GET_PRODUCT_PRICE', int, [product_id])
        del self.products[product_id]
        del self.rating[product_id]

    def increase_rating(self, product_id):
        if product_id not in self.products:
            return
        self.rating[product_id] += 1
        self.rating[product_id] = min(self.rating[product_id], 5)

    def decrease_rating(self, product_id):
        if product_id not in self.products:
            return
        self.rating[product_id] -= 1
        self.rating[product_id] = max(self.rating[product_id], 0)

    def clear_cart(self):
        self.products.clear()
        self.rating.clear()
        self.total_cost = 0

    def is_empty(self):
        return not bool(self.products)
