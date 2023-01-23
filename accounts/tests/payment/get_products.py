from rest_framework.test import APITestCase
from rest_framework import status

class TestGetProducts(APITestCase):

    def test_get_products(self):
        response = self.client.get('/api/v1/stripe/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json())