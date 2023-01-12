from rest_framework.test import APITestCase
from rest_framework import status

from accounts.models.restaurant_user import RestaurantUser

class RestaurantUserSignupUser(APITestCase):

    def setUp(self):
        self.data = {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'password123'
        }

    def test_signup_user_success(self):
        response = self.client.post('/api/v1/restaurant_user/signup/', self.data, format='json')
        self.assertEqual(RestaurantUser.objects.count(), 1)
        self.assertEqual(RestaurantUser.objects.get().username, 'test')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.json().get('token'))

    def test_signup_missing_username(self):
        data = {
            'email': 'test@test.com',
            'password': 'password'
        }

        response = self.client.post('/api/v1/restaurant_user/signup/', data)
        self.assertEqual(RestaurantUser.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_missing_email(self):
        data = {
            'username': 'test',
            'password': 'password'
        }

        response = self.client.post('/api/v1/restaurant_user/signup/', data)
        self.assertEqual(RestaurantUser.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_missing_password(self):
        data = {
            'username': 'test',
            'email': 'test@test.com',
        }
        response = self.client.post('/api/v1/restaurant_user/signup/', data)
        self.assertEqual(RestaurantUser.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_invalid_password(self):
        data = {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'pass'
        }

        response = self.client.post('/api/v1/restaurant_user/signup/', data)
        self.assertEqual(RestaurantUser.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get('error'), 'Password too short')

    def test_signup_error_twice(self):
        response = self.client.post('/api/v1/restaurant_user/signup/', self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.json().get('token'))

        response = self.client.post('/api/v1/restaurant_user/signup/', self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get('error'), 'User already exists')

