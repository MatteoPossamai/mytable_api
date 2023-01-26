from rest_framework.test import APITestCase
from rest_framework import status
from django.core.cache import cache

from accounts.models.restaurant_user import RestaurantUser

from restaurant.models.category import Category
from restaurant.models.restaurant import Restaurant

class CategoryReadSigleTest(APITestCase):

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

    def test_restaurant_get_single(self):
        data = {
            "name": "test",
            "number": 1,
            "isActive": True,
            "restaurant": self.identificator,
            "description": "test"
        }
        response = self.client.post('/api/v1/category/create/', data, format='json', HTTP_TOKEN=self.token)
        identifier = response.json().get('id')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get(id=identifier).name, 'test')

        response = self.client.get(f'/api/v1/category/{identifier}/', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('name'), 'test')

    def test_restaurant_get_single_not_found(self):
        response = self.client.get('/api/v1/category/1001/', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_restaurant_get_single_invalid_id(self):
        response = self.client.get('/api/v1/category/invalid_id/', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_restaurant_get_all_zero(self):
        response = self.client.get('/api/v1/category/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

class CategoryReadAllTest(APITestCase):

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
        for i in range(10):
            Category.objects.create(
                name="test",
                number=i,
                isActive=True,
                restaurant=self.restaurant,
                description="test"
            )

    def test_restaurant_get_all(self):
        response = self.client.get('/api/v1/category/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)


class CategoryReadAllActive(APITestCase):

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
        for i in range(10):
            Category.objects.create(
                name="test",
                number=i,
                isActive=True if i % 2 == 0 else False,
                restaurant=self.restaurant,
                description="test"
            )

    def test_restaurant_get_all_active(self):
        response = self.client.get(f'/api/v1/category/restaurant_category/active/{self.identificator}/', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get('categories')), 5)

        self.assertAlmostEqual(response.json().get('categories')[0].get('name'), 'test')
        self.assertAlmostEqual(response.json().get('categories')[0].get('isActive'), True)
        self.assertAlmostEqual(response.json().get('categories')[0].get('restaurant'), self.identificator)
    
    def test_restaurant_get_all_active_no_auth(self):
        response = self.client.get(f'/api/v1/category/restaurant_category/active/{self.identificator}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    
class CategoryReadAllRestaurant(APITestCase):

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
        for i in range(10):
            Category.objects.create(
                name="test",
                number=i,
                isActive=True if i % 2 == 0 else False,
                restaurant=self.restaurant,
                description="test"
            )

    def test_restaurant_get_all(self):
        response = self.client.get(f'/api/v1/category/restaurant_category/{self.identificator}/', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get('categories')), 10)

        self.assertAlmostEqual(response.json().get('categories')[0].get('name'), 'test')
        self.assertAlmostEqual(response.json().get('categories')[0].get('isActive'), True)
        self.assertAlmostEqual(response.json().get('categories')[0].get('restaurant'), self.identificator)

    def test_restaurant_get_all_active_no_auth(self):
        response = self.client.get(f'/api/v1/category/restaurant_category/{self.identificator}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)