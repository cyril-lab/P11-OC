from unittest import mock
from unittest.mock import patch
from django.test import TestCase
from substitute.services.cleardata import ClearData


class ClearDataTestCase(TestCase):
    """this class test the class cleardata"""
    @patch('substitute.services.requestapi.requests.get')
    def test_get_data_api(self, mock_get):
        mock_response = mock.Mock()
        json = {
            "products": [
                {"product_name_fr": "chocolat",
                 "stores": "super U",
                 "url": "https://url-chocolat",
                 "image_url": "chocolat_url",
                 "nutriscore_grade": "a",
                 "nutriments": {"fat": "10",
                                "saturated-fat_100g": "6",
                                "sugars": "2",
                                "salt": "1"}},
                {"product_name_fr": "lait",
                 # test with a field is empty
                 "stores": "",
                 "url": "https://url-lait",
                 "image_url": "lait_url",
                 "nutriscore_grade": "b",
                 "nutriments": {"fat": "2",
                                "saturated-fat_100g": "3",
                                "sugars": "7",
                                "salt": "2"}}]
                }

        mock_response.json.return_value = json
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        requestapi = ClearData('snack')
        requestapi.get_data_api()
        result = requestapi.generate_products_list()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], 'chocolat')
