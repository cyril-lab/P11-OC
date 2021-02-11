#!/usr/bin/python3

from substitute.services.cleardata import ClearData
from substitute.models.category import Category
from substitute.models.product import Product


class SaveProductDatabase:

    def __init__(self, *args):
        self.category = args

    def main(self):
        for cat in self.category:
            self.save(cat)

    def save(self, category):
        self._save_product(self._save_category(category),
                           self._download_data(category))

    def _save_category(self, category):
        bdd_category = Category(name=category)
        bdd_category.save()
        return bdd_category.id

    def _download_data(self, category):
        products = ClearData(category)
        products.get_number_products()
        products.get_data_api()
        return products.generate_products_list()

    def _save_product(self, category_id, list_product):
        products = list_product
        product_list = sorted(products, key=lambda colonnes: colonnes[4])
        for product_data in product_list:
            product = Product(name=product_data[0],
                              store=product_data[1],
                              url=product_data[2],
                              image_url=product_data[3],
                              nutriscore=product_data[4],
                              nutriment_fat=product_data[5],
                              nutriment_saturated_fat=product_data[6],
                              nutriment_sugars=product_data[7],
                              nutriment_salt=product_data[8],
                              category_id=category_id)
            product.save()
