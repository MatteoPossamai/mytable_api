from rest_framework.test import APITestCase
from rest_framework import status

from accounts.models.restaurant_user import RestaurantUser
from utilities import Encryptor

Encryptor = Encryptor()

class RestaurantUserUpdatePassword(APITestCase):

    def setUp(self):
        self.data = {
            'username': 'test',
            'email': 'test123@test.com',
            'password': 'password11'
        }

        self.data_logged = {
            "user": "test123@test.com",
            'password': '112233ddtest2'
        }

    def test_update_password_success(self):
        # Signup
        response = self.client.post('/api/v1/restaurant_user/signup/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.json().get('token'))
        token = response.json().get('token')

        # Update
        response = self.client.put('/api/v1/restaurant_user/put/password/test123@test.com/', 
            self.data_logged, format='json', HTTP_TOKEN=token)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Check with ORM
        user = RestaurantUser.objects.get(email="test123@test.com")
        self.assertEqual(user.password, Encryptor.encrypt('112233ddtest2'))

    def test_update_password_not_logged(self):
        response = self.client.put('/api/v1/restaurant_user/put/password/test123@test.com/', 
            self.data_logged, format='json', HTTP_TOKEN=None)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_password_another_user(self):
        # Signup
        response = self.client.post('/api/v1/restaurant_user/signup/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.json().get('token'))
        token = response.json().get('token')

        # Update
        response = self.client.put('/api/v1/restaurant_user/put/password/test12223@test.com/', self.data_logged, 
            format='json', HTTP_TOKEN=token)
        self.assertEqual(response.json().get('error'), 'You cannot request to update another user')
    
    def test_update_password_missing_password(self):
        # Signup
        response = self.client.post('/api/v1/restaurant_user/signup/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.json().get('token'))
        token = response.json().get('token')

        bad_data = {
            "user": "test123@test.com",
        }

        # Update
        response = self.client.put('/api/v1/restaurant_user/put/password/test123@test.com/', bad_data, 
            format='json', HTTP_TOKEN=token)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_invalid(self):
        # Signup
        response = self.client.post('/api/v1/restaurant_user/signup/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.json().get('token'))
        token = response.json().get('token')

        bad_data = {
            "user": "test123@test.com",
            'password': '123'
        }
        # Update
        response = self.client.put('/api/v1/restaurant_user/put/password/test123@test.com/', 
            bad_data, format='json', HTTP_TOKEN=token)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get('error'), 'Password too short')
