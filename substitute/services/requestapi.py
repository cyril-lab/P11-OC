#!/usr/bin/python3

import math
import requests


class RequestApi:
    """This class is used to download data from open food facts.
    This class downloads data from the website open food facts using the API.
    Multiple requests are sent until the maximum number entered
    or the number of products is expected.

    """

    def __init__(self, category, number_products_max=100, results_page=100):
        self.number_products_max = number_products_max
        self.category = category
        self.number_products = 1
        self.number_page = 1
        self.results_page = results_page
        self.data_category_json = []
        self.status = 'Not initialized'

    def get_number_products(self):
        """method to get the number of products in the category"""
        number_product_category = \
            requests.get(f"https://fr.openfoodfacts.org/categorie/"
                         f"{self.category}.json")
        number_product_category_json = number_product_category.json()
        self.number_products = int(number_product_category_json["count"])
        return self.number_products

    def calculate_number_page(self):
        """method to calculate the number of pages required for the request"""
        if self.number_products > self.results_page:
            self.number_page = (math.ceil(min(
                self.number_products,
                self.number_products_max) / self.results_page))
        return self.number_page

    def get_data_api(self):
        """method to get data produts"""
        # number_page = self._calculate_number_page()
        while self.number_page:
            data_category = requests.get(
                f"https://fr.openfoodfacts.org/cgi/search.pl?action=process"
                f"&tagtype_0=categories&tag_contains_0=contains&"
                f"tag_0={self.category}&page_size={self.results_page}"
                f"&page={self.number_page}&json=1")

            self.status = data_category.status_code
            self.data_category_json.append(data_category.json())
            self.number_page -= 1
