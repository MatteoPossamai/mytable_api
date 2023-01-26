from rest_framework.test import APITestCase
from rest_framework import status
from django.core.cache import cache

from restaurant.models.restaurant import Restaurant

class RestaurantCreateTest(APITestCase):

    def tearDown(self):
        cache.clear()
        Restaurant.objects.all().delete()

    def setUp(self):
        self.data = {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'password123'
        }
        response = self.client.post('/api/v1/restaurant_user/signup/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.token = response.json().get('token')

    def test_restaurant_create(self):
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

        self.assertEqual(response.json().get('name'), 'test')
        self.assertEqual(response.json().get('location'), 'test')
        self.assertEqual(response.json().get('phone'), 'test')
        self.assertEqual(response.json().get('description'), 'test')
        self.assertEqual(response.json().get('payment_method'), None)
        self.assertEqual(response.json().get('licence_expiration'), None)
        self.assertEqual(response.json().get('owner'), 'test@test.com')

    def test_restaurant_create_without_name(self):
        data = {
            "location": "test",
            "phone": "test",
            "description": "test"
        }
        response = self.client.post('/api/v1/restaurant/create/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_restaurant_create_without_location(self):
        data = {
            "name": "test",
            "phone": "test",
            "description": "test"
        }
        response = self.client.post('/api/v1/restaurant/create/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_restaurant_create_without_phone(self):
        data = {
            "name": "test",
            "location": "test",
            "description": "test"
        }
        response = self.client.post('/api/v1/restaurant/create/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_restaurant_create_without_description(self):
        data = {
            "name": "test",
            "location": "test",
            "phone": "test"
        }
        response = self.client.post('/api/v1/restaurant/create/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_restaurant_create_multiple_instance(self):
        data = {
            "name": "test",
            "location": "test",
            "phone": "test",
            "description": "test"
        }
        i = 0
        for i in range(10):
            data['name'] = 'test' + str(i)
            response = self.client.post('/api/v1/restaurant/create/', data, format='json', HTTP_TOKEN=self.token)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Restaurant.objects.count(), 10)

    def test_restaurant_create_no_auth(self):
        data = {
            "name": "test",
            "location": "test",
            "phone": "test",
            "description": "test"
        }
        response = self.client.post('/api/v1/restaurant/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
