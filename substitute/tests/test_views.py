from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse, resolve
from substitute.models.product import Product
from substitute.models.category import Category
from substitute.views import homepage


class HomePageTest(TestCase):
    """this class test the homepage"""
    def test_root_url_resolves_to_home_page_view(self):
        """this function test the homepage url"""
        response = self.client.get('/')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'substitute/index.html')
        html = response.content.decode('utf8')
        self.assertIn('<title>Accueil</title>', html)


class SearchTestCase(TestCase):
    """this class test the search"""
    def setUp(self):
        Product.objects.create(name="chocolat", category_id=1, nutriscore='a')
        Product.objects.create(name="lait", category_id=1, nutriscore='b')
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

    def test_filter_nutriscore(self):
        """this function test the nutriscrore filter"""
        response = self.client.get("/search/", {'name_product': 'chocolat',
                                                'nutriscore': 'b'})
        self.assertTemplateUsed(response, 'substitute/product.html')
        self.failUnlessEqual(response.status_code, 200)

    def test_filter_vote(self):
        """this function test the vote filter"""
        response = self.client.get("/search/", {'name_product': 'chocolat',
                                                'vote': 'like'})
        self.assertTemplateUsed(response, 'substitute/product.html')
        self.failUnlessEqual(response.status_code, 200)

    def test_filter_vote_and_nutriscore(self):
        """this function test the nutriscrore filter and nutriscore"""
        response = self.client.get("/search/", {'name_product': 'chocolat',
                                                'vote': 'like',
                                                'nutriscore': 'b'})
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


class VoteTest(TestCase):
    """this class test the function named vote"""
    def setUp(self):
        Product.objects.create(id=1,
                               name="chocolat",
                               like=0,
                               dislike=2,
                               category_id=1)
        Category.objects.create(name="snack", id=1)
        self.product = Product.objects.get(id=1)

    def test_like_vote(self):
        """this function test a like vote"""
        self.product = Product.objects.get(id=1)
        self.assertEqual(self.product.like, 0)
        response = self.client.get("/vote/", {'type': 'like',
                                              'value': 1,
                                              'pk': 1})
        self.product = Product.objects.get(id=1)
        self.assertEqual(self.product.like, 1)
        self.failUnlessEqual(response.status_code, 200)

    def test_dislike_vote(self):
        """this function test a dislike vote"""
        self.product = Product.objects.get(id=1)
        self.assertEqual(self.product.dislike, 2)
        response = self.client.get("/vote/", {'type': 'dislike',
                                              'value': 1,
                                              'pk': 1})
        self.product = Product.objects.get(id=1)
        self.assertEqual(self.product.dislike, 3)
        self.failUnlessEqual(response.status_code, 200)
