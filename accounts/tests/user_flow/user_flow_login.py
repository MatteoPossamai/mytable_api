from rest_framework.test import APITestCase
from rest_framework import status

from accounts.models.restaurant_user import RestaurantUser

class RestaurantUserLoginUser(APITestCase):

    def setUp(self):
        self.data = {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'password11'
        }

    def test_login_user_success(self):
        self.client.post('/api/v1/restaurant_user/signup/', self.data, format='json')

        response = self.client.post('/api/v1/restaurant_user/login/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json().get('token'))

    def test_login_user_fail(self):
        response = self.client.post('/api/v1/restaurant_user/login/', self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get('error'), 'User does not exists')

    def test_login_user_missing_email(self):
        data = {
            'username': 'test',
            'password': 'password'
        }

        response = self.client.post('/api/v1/restaurant_user/login/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user_missing_password(self):
        data = {
            'username': 'test',
            'email': 'test@test.com',
        }

        response = self.client.post('/api/v1/restaurant_user/login/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            
