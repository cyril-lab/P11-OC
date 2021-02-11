from django.test import TestCase, Client
from django.urls import reverse
from substitute.models.user import User


class RegisterUser(TestCase):
    """this class test the user registration"""
    def test_create_user_get_form_data(self):
        """this function verify the user creation"""
        self.old_user = User.objects.count()  # count user before a request
        self.form = {'name': 'frederic',
                     'surname': 'durand',
                     'email': 'testmail@orange.fr',
                     'password1': 'mon_mdp',
                     'password2': 'mon_mdp'}
        self.response = self.client.post(reverse('register'),
                                         {'name': self.form['name'],
                                          'surname': self.form['surname'],
                                          'email': self.form['email'],
                                          'password1': self.form['password1'],
                                          'password2': self.form['password2']})
        self.new_user = User.objects.count()  # count user after
        # make sure 1 user was added
        self.assertEqual(self.new_user, self.old_user + 1)

    def test_verify_register(self):
        """this function validate the html code response"""
        response = self.client.post(reverse('register'))
        self.failUnlessEqual(response.status_code, 200)


class LoginUser(TestCase):
    """this class test the user login"""
    def test_login_user_template(self):
        """this function test the template used"""
        client = Client()
        response = client.post('/accounts/login/')
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_account_user_login(self):
        """
        this function test the views,
        the template and the response code of account
        """
        self.client.login(username='jacob', password='top_secret')
        response = self.client.get(reverse('myaccount'))
        self.assertTemplateUsed(response, 'accounts/account.html')
        self.failUnlessEqual(response.status_code, 200)

    def test_logout_user(self):
        """this function test logout redirect"""
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, '/')
