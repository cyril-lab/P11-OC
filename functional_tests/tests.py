import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from substitute.models import User, Product, Category


class SeleniumTest(StaticLiveServerTestCase):
    """this class performs function tests"""
    def setUp(self):
        self.selenium = webdriver.Firefox()

        Category.objects.create(name="snack", id=1)
        Product.objects.create(pk=1,
                               name="chocolat",
                               image_url="url_chocolat",
                               nutriscore="b",
                               category_id=1)

        Product.objects.create(pk=2,
                               name="lait",
                               image_url="url_lait",
                               nutriscore="a",
                               category_id=1)
        Product.objects.create(pk=3,
                               name="biscuit",
                               image_url="url_biscuit",
                               nutriscore="b",
                               category_id=1)

    def tearDown(self):
        self.selenium.quit()

    def test_selenium(self):
        """this function tests website with Selenium"""
        sel = self.selenium
        url = self.live_server_url

        # Test home page
        sel.get(url)
        self.assertIn('Accueil', sel.title)
        time.sleep(2)

        # Test search top
        sel.find_element_by_id("search-header")\
            .send_keys("chocolat", Keys.ENTER)
        sel.implicitly_wait(15)
        element = sel.find_element_by_id("product").text
        self.assertEqual(element, "CHOCOLAT")
        time.sleep(2)

        # Test signup
        sel.get("{}/{}".format(url, "accounts/register"))
        assert "Créer un compte" in sel.title
        sel.find_element_by_id('id_name').send_keys('test_name')
        sel.find_element_by_id('id_surname').send_keys('test_surname')
        sel.find_element_by_id('id_email')\
            .send_keys('adresse_mail@hotmail.fr')
        sel.find_element_by_id('id_password1').send_keys('mdp')
        sel.find_element_by_id('id_password2').send_keys('mdp')
        sel.find_element_by_id("register-btn").click()
        WebDriverWait(sel, 15)
        user = User.objects.get(username='adresse_mail@hotmail.fr')
        self.assertEqual(user.username, 'adresse_mail@hotmail.fr')
        self.assertEqual(user.first_name, 'test_name')
        time.sleep(2)

        # Test login
        sel.get("{}/{}".format(self.live_server_url, "accounts/login"))
        self.assertIn('Me connecter', sel.title)
        sel.find_element_by_name('username')\
            .send_keys('adresse_mail@hotmail.fr')
        sel.find_element_by_name('password').send_keys('mdp')
        sel.find_element_by_id("login-btn").click()
        time.sleep(1)

        # Test favorites
        sel.get("{}/{}".format(self.live_server_url, "favorite"))
        self.assertIn('Favoris', sel.title)
        time.sleep(2)

        # Test search botton
        sel.get(url)
        sel.find_element_by_id("search").send_keys("chocolat", Keys.ENTER)
        sel.implicitly_wait(15)
        element = sel.find_element_by_id("product").text
        self.assertEqual(element, "CHOCOLAT")
        self.assertIn('Produits', sel.title)
        time.sleep(2)

        # Test product detail
        sel.find_element_by_class_name("card-title").click()
        self.assertIn('Détail produit', sel.title)
        time.sleep(2)
        sel.find_element_by_class_name("btn").click()
        self.assertIn('Favoris', sel.title)

        # Test add favorites
        time.sleep(2)
        element = sel.find_element_by_class_name("card-title").text
        self.assertEqual(element, "lait")

        # Test logout
        sel.find_element_by_id("logout-btn").click()
        sel.get("{}/{}".format(self.live_server_url, "favorite"))
        self.assertIn('Accueil', sel.title)
        time.sleep(2)
