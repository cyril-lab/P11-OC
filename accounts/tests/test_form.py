from django.test import TestCase
from ..forms import CreateUserForm


class CreateUserFormTest(TestCase):
    """this class test the form CreateUserForm"""
    def setUp(self):
        self.user_email = "test@orange.fr"
        self.data = {"email": "test@orange.fr",
                     "password1": "password1",
                     "password2": "password2",
                     "name": "cyril",
                     "surname": "surname"}
        self.form = CreateUserForm(self.data)

    def test_max_length(self):
        """this function test the max length of the field name"""
        self.assertEquals(self.form.fields["name"].max_length, 100)

    def test_valid_true_email(self):
        """
        this function test the email validity,
        test is ok if email is correct
        """
        self.assertTrue(self.form.is_valid())

    def test_valid_false_email(self):
        """
         this function test the email validity,
        test is ok if email is NOT correct
        """
        self.data['email'] = "emailnotcorrect.fr"
        self.form = CreateUserForm(self.data)
        self.assertFalse(self.form.is_valid())
