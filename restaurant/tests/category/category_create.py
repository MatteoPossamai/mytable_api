from rest_framework.test import APITestCase
from rest_framework import status
from django.core.cache import cache

from restaurant.models.category import Category
from restaurant.models.restaurant import Restaurant
from accounts.models import RestaurantUser

class CategoryCreateTest(APITestCase):
    
    def tearDown(self):
        cache.clear()
        Category.objects.all().delete()
        Restaurant.objects.all().delete()
        RestaurantUser.objects.all().delete()

    def setUp(self):
        cache.clear()
        self.data = {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'password123'
        }
        response = self.client.post('/api/v1/restaurant_user/signup/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.token = response.json().get('token')

        self.user = RestaurantUser.objects.get(username='test')

        self.restaurant = Restaurant.objects.create(
            name="test",
            location="test",
            phone="test",
            owner=self.user,
        )
        self.identificator = self.restaurant.id

    def test_category_create(self):

        data = {
            "name": "test",
            "number": 1,
            "isActive": True,
            "restaurant": self.identificator,
            "description": "test"
        }
        response = self.client.post('/api/v1/category/create/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get().name, 'test')
        data = response.json()
        self.assertEqual(data['name'], 'test')
        self.assertEqual(data['number'], 1)
        self.assertEqual(data['isActive'], True)
        self.assertEqual(data['description'], 'test')
        self.assertEqual(data['restaurant'], self.identificator)

    def test_create_category_multiple(self):
        i = 0
        number_of_categories = 10
        data = {
            "name": "test",
            "number": 1,
            "isActive": True,
            "restaurant": self.identificator,
            "description": "test"
        }

        for i in range(number_of_categories):
            data["name"] = f"test{i}"
            response = self.client.post('/api/v1/category/create/', data, format='json', HTTP_TOKEN=self.token)
            identifier = response.json().get('id')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Category.objects.count(), i+1)
            self.assertEqual(Category.objects.get(id=identifier).name, f'test{i}')

    def test_create_category_no_name(self):
        data = {
            "number": 1,
            "isActive": True,
            "description": "test"
        }
        response = self.client.post('/api/v1/category/create/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_category_no_number(self):
        data = {
            "name": "test",
            "isActive": True,
            "description": "test"
        }
        response = self.client.post('/api/v1/category/create/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_category_no_isActive(self):
        data = {
            "name": "test",
            "number": 1,
            "description": "test"
        }
        response = self.client.post('/api/v1/category/create/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_category_no_description(self):
        data = {
            "name": "test",
            "number": 1,
            "isActive": True,
        }
        response = self.client.post('/api/v1/category/create/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_category_bad_number_type(self):
        data = {
            "name": "test",
            "number": "1",
            "isActive": True,
            "restaurant": self.identificator,
            "description": "test"
        }
        response = self.client.post('/api/v1/category/create/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)

    def test_create_category_no_auth(self):
        response = self.client.post('/api/v1/category/create/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        