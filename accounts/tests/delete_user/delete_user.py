from rest_framework.test import APITestCase
from rest_framework import status

from accounts.models.restaurant_user import RestaurantUser

class RestaurantUserDelete(APITestCase):

    def setUp(self):
        self.data = {
            'username': 'test',
            'email': 'test123@test.com',
            'password': 'password11'
        }

        self.data_logged = {
            "user": "test123@test.com"
        }

    def test_delete_success(self):
        # Signup
        response = self.client.post('/api/v1/restaurant_user/signup/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.json().get('token'))
        token = response.json().get('token')

        # Check with ORM
        self.assertEqual(RestaurantUser.objects.count(), 1)

        # Delete
        response = self.client.post("/api/v1/restaurant_user/delete/test123@test.com/", self.data_logged, 
            format='json', HTTP_TOKEN=token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check with ORM
        self.assertEqual(RestaurantUser.objects.count(), 0)

    def test_delete_not_logged(self):
        # Delete
        response = self.client.post("/api/v1/restaurant_user/delete/test123@test.com/", self.data_logged, 
            format='json', HTTP_TOKEN=None)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_another_user(self):
        # Signup
        response = self.client.post('/api/v1/restaurant_user/signup/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.json().get('token'))
        token = response.json().get('token')

        # Check with ORM
        self.assertEqual(RestaurantUser.objects.count(), 1)

        # Delete
        response = self.client.post("/api/v1/restaurant_user/delete/test13@test.com/", self.data_logged, 
            format='json', HTTP_TOKEN=token)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json().get('error'), 'You cannot request to delete another user')