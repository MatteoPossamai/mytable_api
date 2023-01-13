from rest_framework.test import APITestCase
from rest_framework import status

from accounts.models.restaurant_user import RestaurantUser

class RestaurantUserCompleteFlow(APITestCase):

    def setUp(self):
        self.data = {
            'username': 'test',
            'email': 'test123@test.com',
            'password': 'password11'
        }

        self.data_logged = {
            "user": "test123@test.com"
        }

    def test_complete_1(self):
        # Create the user
        response = self.client.post('/api/v1/restaurant_user/signup/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.json().get('token'))
        token = response.json().get('token')

        # Check if logged
        response = self.client.post('/api/v1/restaurant_user/logged/', data=self.data_logged, format='json', HTTP_TOKEN=token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Logout
        response = self.client.post('/api/v1/restaurant_user/logout/', data=self.data_logged, format='json', HTTP_TOKEN=token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check if logged
        response = self.client.post('/api/v1/restaurant_user/logged/', data=self.data_logged, format='json', HTTP_TOKEN=token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Login
        response = self.client.post('/api/v1/restaurant_user/login/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json().get('token'))
        token = response.json().get('token')

        # Check if logged
        response = self.client.post('/api/v1/restaurant_user/logged/', data=self.data_logged, format='json', HTTP_TOKEN=token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_complete_2(self):
        # Create 
        response = self.client.post('/api/v1/restaurant_user/signup/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.json().get('token'))
        token = response.json().get('token')

        # Logout
        response = self.client.post('/api/v1/restaurant_user/logout/', data=self.data_logged, format='json', HTTP_TOKEN=token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Logout
        response = self.client.post('/api/v1/restaurant_user/logout/', data=self.data_logged, format='json', HTTP_TOKEN=token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Check if logged
        response = self.client.post('/api/v1/restaurant_user/logged/', data=self.data_logged, format='json', HTTP_TOKEN=token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Login
        response = self.client.post('/api/v1/restaurant_user/login/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json().get('token'))
        token = response.json().get('token')

        # Check if logged
        response = self.client.post('/api/v1/restaurant_user/logged/', data=self.data_logged, format='json', HTTP_TOKEN=token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Login
        response = self.client.post('/api/v1/restaurant_user/login/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json().get('token'))
        token = response.json().get('token')

        # Check if logged
        response = self.client.post('/api/v1/restaurant_user/logged/', data=self.data_logged, format='json', HTTP_TOKEN=token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)