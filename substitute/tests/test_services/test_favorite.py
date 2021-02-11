from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory
from django.urls import reverse
from substitute.models.product import Product
from substitute.models.user import User
from substitute.models.category import Category
from substitute.services.favorite import Favorite


class SaveFavoriteTestCase(TestCase):
    """this class test the save favorite user case"""
    def setUp(self):
        Product.objects.create(pk=1,
                               name="biscuit",
                               image_url="url_biscuit",
                               nutriscore="b",
                               category_id=1)
        Category.objects.create(name="snack", id=1)
        self.factory = RequestFactory()
        self.user = User.objects.create_user(pk=1,
                                             username='jacob',
                                             email='jacob@orange.fr',
                                             password='top_secret')
        self.request = self.factory.get("save-favorite/1")
        self.favorite = Favorite(self.request, pk_prod=1)
        self.request.user = self.user

    def test_login_validate(self):
        """you must be authenticated to add a favorite"""
        # the user is logged in
        self.assertTrue(self.favorite.login_validate())
        # the user is logged out
        self.request.user = AnonymousUser()
        self.assertFalse(self.favorite.login_validate())

    def test_saved_favorite(self):
        """the function must add the favorites in the database"""
        self.favorite.saved_favorite()
        favorite_sub = Product.objects.get(favorite__id=1)
        self.assertEquals(favorite_sub.name, 'biscuit')

    def test_return_favorite_list(self):
        """the function must return a list"""
        self.favorite.saved_favorite()
        favorite_list = self.favorite.return_favorite_list()
        self.assertEqual(len(favorite_list), 1)
        self.assertEqual(favorite_list[0][0], 1)
        self.assertEqual(favorite_list[0][1], 'biscuit')
        self.assertEqual(favorite_list[0][2], 'url_biscuit')
        self.assertEqual(favorite_list[0][3], 'b')

    def test_view_save_favorite(self):
        """save favorite if the user is logged in"""
        self.client.login(username='jacob', password='top_secret')
        response = self.client.get(reverse('save_favorite',
                                           kwargs={'pk_prod': 1}))
        self.assertTemplateUsed(response, 'substitute/favorite.html')
        self.failUnlessEqual(response.status_code, 200)