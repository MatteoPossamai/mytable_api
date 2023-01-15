from rest_framework.test import APITestCase
from rest_framework import status
from django.core.cache import cache

from restaurant.models.category import Category
from restaurant.models.restaurant import Restaurant
from accounts.models import RestaurantUser

class CategoryUpdateTest(APITestCase):

    def tearDown(self):
        cache.clear()

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
            plan={},
            location="test",
            phone="test",
            owner=self.user,
        )
        self.identificator = self.restaurant.id
        Category.objects.create(
            name="test",
            number=1,
            isActive=True,
            restaurant=self.restaurant,
            description="test"
        )

        for i in range(10):
            Category.objects.create(
                name=f"test{i}",
                number=i,
                isActive=True if i % 2 == 0 else False,
                restaurant=self.restaurant,
                description=f"test{i}"
            )

    def test_restaurant_update(self):
        category = Category.objects.get(name="test")
        identifier = category.id
        data = {
            "name": "test",
            "number": 1,
            "isActive": True,
            "restaurant": self.restaurant.id,
            "description": "test"
        }
        response = self.client.put(f'/api/v1/category/put/{identifier}/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.count(), 11)
        self.assertEqual(Category.objects.get(id=identifier).name, 'test')

    def test_restaurant_update_not_found(self):
        data = {
            "name": "test",
            "number": 1,
            "isActive": True,
            "restaurant": self.restaurant.id,
            "description": "test"
        }
        response = self.client.put('/api/v1/category/put/255/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_restaurant_update_invalid_id(self):
        data = {
            "name": "test",
            "number": 1,
            "isActive": True,
            "restaurant": self.restaurant.id,
            "description": "test"
        }
        response = self.client.put('/api/v1/category/put/invalid_id/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_restaurant_update_invalid_data(self):
        category = Category.objects.get(name="test")
        identifier = category.id
        data = {
            "name": "test",
            "number": 1,
            "isActive": True,
            "restaurant": self.restaurant.id,
            "description": "test"
        }
        response = self.client.put(f'/api/v1/category/put/{identifier}/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.count(), 11)
        self.assertEqual(Category.objects.get(id=identifier).name, 'test')

        data = {
            "name": "test",
            "restaurant": self.restaurant.id,
            "description": "test"
        }
        response = self.client.put(f'/api/v1/category/put/{identifier}/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Category.objects.count(), 11)
        self.assertEqual(Category.objects.get(id=identifier).name, 'test')

    def test_restaurant_update_invalid_data_2(self):
        category = Category.objects.get(name="test")
        identifier = category.id
        data = {
            "name": "test",
            "number": 1,
            "isActive": True,
            "restaurant": self.restaurant.id,
            "description": "test"
        }
        response = self.client.put(f'/api/v1/category/put/{identifier}/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.count(), 11)
        self.assertEqual(Category.objects.get(id=identifier).name, 'test')

        data = {
            "name": "test",
            "number": 1,
        }
        response = self.client.put(f'/api/v1/category/put/{identifier}/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Category.objects.count(), 11)
        self.assertEqual(Category.objects.get(id=identifier).name, 'test')

    def test_restaurant_update_change_number(self):
        category = Category.objects.get(name="test")
        identifier = category.id
        data = {
            "categories": [
                {
                    "id": identifier,
                    "number": 2,
                    "restaurant": self.restaurant.id,
                    "isActive": True,
                }
            ]
        }
        response = self.client.put(f'/api/v1/category/change-number/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 11)
        self.assertEqual(Category.objects.get(id=identifier).name, 'test')
        self.assertEqual(Category.objects.get(id=identifier).number, 2)

    def test_restaurant_update_change_number_invalid_data(self):
        category = Category.objects.get(name="test")
        identifier = category.id
        data = {
            "categories": [
                {
                    "id": identifier,
                    "number": 2
                }
            ]
        }
        response = self.client.put(f'/api/v1/category/change-number/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Category.objects.count(), 11)
        self.assertEqual(Category.objects.get(id=identifier).name, 'test')
        self.assertEqual(Category.objects.get(id=identifier).number, 1)

        data = {
            "categories": [
                {
                    "id": identifier,
                }
            ]
        }
        response = self.client.put(f'/api/v1/category/change-number/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Category.objects.count(), 11)
        self.assertEqual(Category.objects.get(id=identifier).name, 'test')
        self.assertEqual(Category.objects.get(id=identifier).number, 1)

    def test_restaurant_update_change_active(self):
        category = Category.objects.get(name="test")
        identifier = category.id
        data = {
            "categories": [
                {
                    "id": identifier,
                    "isActive": False
                }
            ]
        }
        response = self.client.put(f'/api/v1/category/change-active/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Category.objects.count(), 11)
        self.assertEqual(Category.objects.get(id=identifier).name, 'test')
        self.assertEqual(Category.objects.get(id=identifier).isActive, True)

    def test_restaurant_update_change_active_invalid_data(self):
        category = Category.objects.get(name="test")
        identifier = category.id
        data = {
            "categories": [
                {
                    "id": identifier,
                    "isActive": 'ciao'
                }
            ]
        }
        response = self.client.put(f'/api/v1/category/change-active/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            "categories": [
                {
                    "id": identifier,
                }
            ]
        }
        response = self.client.put(f'/api/v1/category/change-active/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Category.objects.count(), 11)
        self.assertEqual(Category.objects.get(id=identifier).name, 'test')
        self.assertEqual(Category.objects.get(id=identifier).isActive, True)

    def test_category_update_no_auth(self):
        response = self.client.put(f'/api/v1/category/put/1/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_category_update_number_no_auth(self):
        response = self.client.put(f'/api/v1/category/change-number/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_category_update_active_no_auth(self):
        response = self.client.put(f'/api/v1/category/change-active/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_category_bulk_update_no_auth(self):
        response = self.client.put(f'/api/v1/category/bulk_update/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_category_bulk_update(self):
        category = Category.objects.get(name="test")
        identifier = category.id
        data = {
            "categories": [
                {
                    "id": identifier,
                    "name": "test2",
                    "number": 2,
                    "restaurant": self.restaurant.id,
                    "isActive": True,
                }
            ]
        }
        response = self.client.put(f'/api/v1/category/bulk_update/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_category_bulk_update_invalid_data(self):
        category = Category.objects.get(name="test")
        identifier = category.id
        data = {
            "categories": [
                {
                    "id": identifier,
                    "name": "test2",
                    "number": 2,
                    "restaurant": self.restaurant.id,
                    "isActive": 'ciao',
                }
            ]
        }
        response = self.client.put(f'/api/v1/category/bulk_update/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
