from rest_framework.test import APITestCase
from rest_framework import status
from django.core.cache import cache

from restaurant.models.restaurant import Restaurant

class RestaurantDeleteTest(APITestCase):

    def tearDown(self):
        cache.clear()
        Restaurant.objects.all().delete()

    def setUp(self):
        self.data = {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'password123'
        }
        self.data_logged = {
            "user": "test@test.com"
        }
        response = self.client.post('/api/v1/restaurant_user/signup/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.token = response.json().get('token')

    def test_restaurant_delete(self):
        data = {
            "name": "test",
            "location": "test",
            "phone": "test",
            "description": "test"
        }
        response = self.client.post('/api/v1/restaurant/create/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertEqual(Restaurant.objects.get().name, 'test')
        identification = Restaurant.objects.get().id
        response = self.client.delete(f'/api/v1/restaurant/delete/{identification}/', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_restaurant_delete_not_found(self):
        response = self.client.delete('/api/v1/restaurant/delete/1/', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_restaurant_delete_no_auth(self):
        # Logout
        response = self.client.post('/api/v1/restaurant_user/logout/', data=self.data_logged, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Delete
        response = self.client.delete('/api/v1/restaurant/delete/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)