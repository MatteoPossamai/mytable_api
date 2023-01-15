from rest_framework.test import APITestCase
from rest_framework import status
from django.core.cache import cache

from restaurant.models.restaurant import Restaurant

class RestaurantPutTest(APITestCase):

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
            "user": "test123@test.com"
        }
        response = self.client.post('/api/v1/restaurant_user/signup/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.token = response.json().get('token')

    def test_restaurant_put_success(self):
        data = {
            "name": "test",
            "plan": {},
            "location": "test",
            "phone": "test",
            "description": "test"
        }
        response = self.client.post('/api/v1/restaurant/create/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        identification = Restaurant.objects.get().id
        data = {
            "name": "test2",
            "plan": {"test": "test"},
            "location": "test2",
            "phone": "test2",
            "description": "test2"
        }
        response = self.client.put(f'/api/v1/restaurant/put/{identification}/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertEqual(Restaurant.objects.get().name, 'test2')
        self.assertEqual(Restaurant.objects.get().plan, {"test": "test"})
        self.assertEqual(Restaurant.objects.get().location, 'test2')
        self.assertEqual(Restaurant.objects.get().phone, 'test2')
        self.assertEqual(Restaurant.objects.get().description, 'test2')


    def test_restaurant_put_not_found(self):
        data = {
            "name": "test",
            "plan": {},
            "location": "test",
            "phone": "test",
            "description": "test"
        }
        response = self.client.put('/api/v1/restaurant/put/1/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_restaurant_put_no_auth(self):
        response = self.client.put('/api/v1/restaurant/put/1/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_restaurant_put_bad_request(self):
        data = {
            "name": "test",
            "plan": {},
            "location": "test",
            "phone": "test",
            "description": "test"
        }
        response = self.client.post('/api/v1/restaurant/create/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertEqual(Restaurant.objects.get().name, 'test')
        identification = Restaurant.objects.get().id
        data = {
            "name": "test2",
            "plan": {},
            "location": "test2",
            "phone": "test2",
            "description": "test2"
        }
        response = self.client.put(f'/api/v1/restaurant/put/{identification}/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertEqual(Restaurant.objects.get().name, 'test2')
        data = {
            "plan": 1,
            "description": "test3"
        }
        response = self.client.put(f'/api/v1/restaurant/put/{identification}/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertEqual(Restaurant.objects.get().name, 'test2')

    def test_restaurant_put_change_plan(self):
        data = {
            "name": "test",
            "plan": {},
            "location": "test",
            "phone": "test",
            "description": "test"
        }
        response = self.client.post('/api/v1/restaurant/create/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertEqual(Restaurant.objects.get().name, 'test')
        identification = Restaurant.objects.get().id

        data = {
            "plan": {'test': 'test'}
        }

        response = self.client.put(f'/api/v1/restaurant/change-plan/{identification}/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertEqual(Restaurant.objects.get().plan, {'test': 'test'})

    def test_restaurant_put_change_plan_bad_request(self):
        data = {
            "name": "test",
            "plan": {},
            "location": "test",
            "phone": "test",
            "description": "test"
        }
        response = self.client.post('/api/v1/restaurant/create/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertEqual(Restaurant.objects.get().name, 'test')
        identification = Restaurant.objects.get().id

        data = {}

        response = self.client.put(f'/api/v1/restaurant/change-plan/{identification}/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertEqual(Restaurant.objects.get().plan, {})

    def test_restaurant_put_change_plan_not_found(self):
        data = {}

        response = self.client.put(f'/api/v1/restaurant/change-plan/1/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_restaurant_put_change_plan_no_auth(self):
        data = {}

        response = self.client.put(f'/api/v1/restaurant/change-plan/1/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)