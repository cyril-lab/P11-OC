from unittest import mock
from unittest.mock import patch
from django.test import TestCase
from substitute.services.requestapi import RequestApi


class RequestApiTestCase(TestCase):
    """this class test the class requestapi"""
    @patch('substitute.services.requestapi.requests.get')
    def test_get_number_products(self, mock_get):
        """this function test the function get_number_products()"""
        mock_response = mock.Mock()
        json = {"count": "1001"}
        mock_response.json.return_value = json
        mock_response.status_code = 200
        # Define response for the fake API
        mock_get.return_value = mock_response
        requestapi = RequestApi('snack')
        result = requestapi.get_number_products()
        self.assertEqual(result, 1001)

    def test_calculate_number_page(self):
        """this function test the function calculate_number_page()"""
        self.requestapi = RequestApi('snack')
        result = self.requestapi.calculate_number_page()
        self.assertEqual(result, 1)

    def test_calculate_number_page_number_products_max_different(self):
        """
        this function test the function calculate_number_page()
        number_products_max=1000
        """
        self.requestapi = RequestApi('snack', number_products_max=1000)
        self.requestapi.number_products = 1000
        result = self.requestapi.calculate_number_page()
        self.assertEqual(result, 10)

    def test_calculate_number_page_results_page_different(self):
        """
        this function test the function calculate_number_page()
        number_products_max=1000
        results_page=500
        """
        self.requestapi = RequestApi('snack', number_products_max=1000,
                                     results_page=500)
        self.requestapi.number_products = 1000
        result = self.requestapi.calculate_number_page()
        self.assertEqual(result, 2)
