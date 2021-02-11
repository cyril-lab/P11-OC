from django.test import TestCase, RequestFactory
from django.urls import reverse
from substitute.models.product import Product
from substitute.models.category import Category
from substitute.services.searchsubstitute import SearchSubstitute
from django.db.models.query import QuerySet


class SearchSubstituteTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name="chocolat",
                               image_url="url_chocolat",
                               nutriscore="b",
                               category_id=1)
        Product.objects.create(name="lait",
                               image_url="url_lait",
                               nutriscore="a",
                               category_id=1)
        Product.objects.create(name="biscuit",
                               image_url="url_biscuit",
                               nutriscore="b",
                               category_id=2)
        Category.objects.create(name="snack", id=1)
        Category.objects.create(name="fromage", id=2)
        self.factory = RequestFactory()
        self.request = self.factory.get(
            reverse("search", kwargs={}), {"name_product": "chocolat"})
        self.search = SearchSubstitute(self.request)

    def test_query_get_product_name(self):
        """test request product"""
        result = self.search._query_get_product_name()
        self.assertEqual(result, "chocolat")

    def test_save_search_product(self):
        """test saved request product"""
        search_product = self.search._save_search_product()
        self.assertEqual(type(search_product), QuerySet)

    def test_validate_search_product(self):
        """test validate_search_product() method"""
        self.assertTrue(self.search.validate_search_product())

    def test_get_product_substitute(self):
        """test get_product_substitute() method"""
        result = self.search.get_product_substitute()
        self.assertEqual(len(result), 1)
