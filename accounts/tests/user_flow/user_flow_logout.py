from rest_framework.test import APITestCase
from rest_framework import status

from accounts.models.restaurant_user import RestaurantUser

class RestaurantUserLogoutUser(APITestCase):

    def setUp(self):
        self.data = {
            'username': 'test',
            'email': 'test123@test.com',
            'password': 'password11'
        }

        self.data_logged = {
            "user": "test123@test.com"
        }

    def test_logout_with_success(self):
        response = self.client.post('/api/v1/restaurant_user/signup/', self.data, format='json')
        token = response.json().get('token')

        response = self.client.post('/api/v1/restaurant_user/logout/', data=self.data_logged, format='json', HTTP_TOKEN=token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_not_logged(self):
        response = self.client.post('/api/v1/restaurant_user/logout/', data=self.data_logged, format='json', HTTP_TOKEN=None)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)