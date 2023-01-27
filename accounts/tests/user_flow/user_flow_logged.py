from rest_framework.test import APITestCase
from rest_framework import status

from accounts.models.restaurant_user import RestaurantUser

class RestaurantUserLoggedUser(APITestCase):

    def setUp(self):
        self.data = {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'password11'
        }

        self.data_logged = {
            "user": "test@test.com"
        }

    def test_logged_user_success(self):
        response = self.client.post('/api/v1/restaurant_user/signup/', self.data, format='json')
        token = response.json().get('token')

        response = self.client.post('/api/v1/restaurant_user/logged/', data=self.data_logged, format='json', HTTP_TOKEN=token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_logged_not_logged(self):
        response = self.client.post('/api/v1/restaurant_user/logged/', data=self.data_logged, format='json', HTTP_TOKEN=None)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)