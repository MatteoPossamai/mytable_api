from rest_framework.test import APITestCase
from rest_framework import status

from accounts.models.restaurant_user import RestaurantUser

class RestaurantUserUpdateUsername(APITestCase):

    def setUp(self):
        self.data = {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'password11'
        }

        self.data_logged = {
            "user": "test@test.com",
            'username': 'test2'
        }

    def test_update_username_success(self):
        # Signup
        response = self.client.post('/api/v1/restaurant_user/signup/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.json().get('token'))
        token = response.json().get('token')

        # Update
        response = self.client.put('/api/v1/restaurant_user/put/', self.data_logged, format='json', HTTP_TOKEN=token)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check with ORM
        user = RestaurantUser.objects.get(email="test@test.com")
        self.assertEqual(user.username, 'test2')

    def test_update_username_not_logged(self):
        response = self.client.put('/api/v1/restaurant_user/put/', self.data_logged, 
            format='json', HTTP_TOKEN=None)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_username_missing_username(self):
        # Signup
        response = self.client.post('/api/v1/restaurant_user/signup/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.json().get('token'))
        token = response.json().get('token')

        bad_data = {
            "user": "test@test.com",
        }

        # Update
        response = self.client.put('/api/v1/restaurant_user/put/', bad_data, 
            format='json', HTTP_TOKEN=token)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_like_another_user(self):
        # Signup
        response = self.client.post('/api/v1/restaurant_user/signup/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.json().get('token'))
        token = response.json().get('token')

        data2 = {
            'username': 'test2',
            'email': 'test123@test.com',
            'password': 'password11'
        }
        
        response = self.client.post('/api/v1/restaurant_user/signup/', data2, format='json')

        response = self.client.put('/api/v1/restaurant_user/put/', self.data_logged, 
            format='json', HTTP_TOKEN=token)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get('error'), 'Username already exists')


