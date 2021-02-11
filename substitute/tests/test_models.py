from django.test import TestCase
from substitute.models.product import Product
from substitute.models.user import User
from substitute.models.category import Category


class ProductTest(TestCase):
    """this class test the product model"""
    def setUp(self):
        Product.objects.create(id=1, name="chocolat", category_id=1)
        Category.objects.create(name="snack", id=1)
        self.product = Product.objects.get(id=1)

    def test_product_saved(self):
        """this function tests if the product is registered """
        self.assertEqual(self.product.name, 'chocolat')

    def test_product_label(self):
        """this function tests field product label """
        field_label = self.product._meta.get_field("name").verbose_name
        self.assertEquals(field_label, "name")


class CategoryTest(TestCase):
    """this class test the category model"""
    def setUp(self):
        Category.objects.create(name="snack", id=1)
        self.category = Category.objects.get(id=1)

    def test_category_saved(self):
        """this function tests if the category is registered """
        self.assertEqual(self.category.name, 'snack')

    def test_category_label(self):
        """this function tests field category label """
        field_label = self.category._meta.get_field("name").verbose_name
        self.assertEquals(field_label, "name")


class UserTest(TestCase):
    """this class test the user model"""
    def setUp(self):
        User.objects.create(username="jack", id=1)

    def test_user_saved(self):
        """this function tests if the user is registered """
        user = User.objects.get(id=1)
        self.assertEqual(user.username, 'jack')
