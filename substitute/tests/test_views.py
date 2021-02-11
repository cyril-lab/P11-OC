from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.test import TestCase, RequestFactory
from django.urls import reverse, resolve
from substitute.models.product import Product
from substitute.models.user import User
from substitute.models.category import Category
from substitute.views import homepage
from substitute.services.favorite import Favorite


class HomePageTest(TestCase):
    """this class test the homepage"""
    def test_root_url_resolves_to_home_page_view(self):
        """this function test the homepage url"""
        found = resolve('/')
        self.assertEqual(found.func, homepage)

    def test_home_page_returns_correct_html(self):
        """this function test the homepage html"""
        request = HttpRequest()
        response = homepage(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>Accueil</title>', html)


class SearchTestCase(TestCase):
    """this class test the search"""
    def setUp(self):
        Product.objects.create(name="chocolat", category_id=1)
        Product.objects.create(name="lait", category_id=1)
        Category.objects.create(name="snack", id=1)

    def test_template_return_unregistered_product(self):
        """this function test the unregistered product"""
        response = self.client.get("/search/", {'name_product': 'biscuit'})
        self.assertTemplateUsed(response, 'substitute/no_result.html')
        self.failUnlessEqual(response.status_code, 200)

    def test_template_return_registered_product(self):
        """this function test the registered product"""
        response = self.client.get("/search/", {'name_product': 'chocolat'})
        self.assertTemplateUsed(response, 'substitute/product.html')
        self.failUnlessEqual(response.status_code, 200)


class ProductTestCase(TestCase):
    """class product test"""
    def setUp(self):
        Product.objects.create(pk=1, name="chocolat", category_id=1)
        Category.objects.create(name="snack", id=1)

    def test_product_404(self):
        """non-existent product number test"""
        response = self.client.get(reverse('product',
                                           kwargs={'pk': 676767676}))
        self.assertTemplateUsed(response, '404.html')
        self.failUnlessEqual(response.status_code, 404)

    def test_product_200(self):
        """existent product number test"""
        response = self.client.get(reverse('product', kwargs={'pk': 1}))
        self.assertTemplateUsed(response, 'substitute/product_detail.html')
        self.failUnlessEqual(response.status_code, 200)
