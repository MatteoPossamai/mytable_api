from rest_framework.test import APITestCase
from rest_framework import status

class RestaurantUserLogoutUser(APITestCase):

    def setUp(self):
        self.data = {
            'username': 'test',
            'email': 'test123@test.com',
            'password': 'password11'
        }

    def test_logout_with_success(self):
        response = self.client.post('/api/v1/restaurant_user/signup/', self.data, format='json')
        token = response.json().get('token')

        response = self.client.post('/api/v1/restaurant_user/logout/', format='json', HTTP_TOKEN=token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_logout_not_logged(self):
        response = self.client.post('/api/v1/restaurant_user/logout/', format='json', HTTP_TOKEN=None)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)