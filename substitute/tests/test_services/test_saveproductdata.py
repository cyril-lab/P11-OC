from django.test import TestCase
from substitute.services.saveproductdatabase import SaveProductDatabase
from substitute.models.category import Category


class SaveProductDatabaseTestCase(TestCase):
    """this class test the class saveproductdatabase"""
    def setUp(self):
        Category.objects.create(name="snack")

    def test_save_category(self):
        """this function tests the recording of a category"""
        self.old_category = Category.objects.count()
        category = SaveProductDatabase()
        category._save_category("snack")
        self.new_category = Category.objects.count()  # count user after
        # make sure one category was added
        self.assertEqual(self.new_category, self.old_category + 1)
