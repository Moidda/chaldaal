from django.db import models


class Cart:
    products = {}

    def add_product(self, product_id):
        if product_id in self.products:
            self.products[product_id] += 1
        else:
            self.products[product_id] = 1

    def remove_product(self, product_id):
        if product_id not in self.products:
            return
        self.products[product_id] -= 1
        self.products[product_id] = max(self.products[product_id], 0)

    def erase_product(self, product_id):
        if product_id not in self.products:
            return
        del self.products[product_id]

    def clear_cart(self):
        self.products.clear()