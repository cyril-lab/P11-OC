#!/usr/bin/python3

from substitute.services.requestapi import RequestApi


class ClearData(RequestApi):
    """This class converts the retrieved data"""

    def generate_products_list(self):
        """method to generate a list with products"""
        products = []
        for request in self.data_category_json:
            for product in request["products"]:
                nutriment = product.get("nutriments")
                if product.get("product_name_fr") \
                        and product.get("stores") \
                        and product.get("url") \
                        and product.get("image_url") \
                        and product.get("nutriscore_grade") \
                        and nutriment.get("fat") \
                        and nutriment.get("saturated-fat_100g") \
                        and nutriment.get("sugars") \
                        and nutriment.get("salt") is not None \
                        and len(products) < self.number_products_max:

                    products.extend([[product.get("product_name_fr"),
                                      product.get("stores"),
                                      product.get("url"),
                                      product.get("image_url"),
                                      product.get("nutriscore_grade"),
                                      nutriment.get("fat"),
                                      nutriment.get("saturated-fat_100g"),
                                      nutriment.get("sugars"),
                                      nutriment.get("salt")]])

        return products
