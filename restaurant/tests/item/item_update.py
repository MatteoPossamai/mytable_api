from rest_framework.test import APITestCase
from rest_framework import status
from django.core.cache import cache

from restaurant.models.category import Category
from restaurant.models.item import Item
from restaurant.models.restaurant import Restaurant
from accounts.models import RestaurantUser


class ItemUpdateTest(APITestCase):

    def setUp(self):
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
        self.id = self.restaurant.id
        self.category = Category.objects.create(
            name="test",
            number=1,
            isActive=True,
            restaurant=self.restaurant,
            description="test"
        )
        self.cat = self.category.id
        self.item = Item.objects.create(
            category=self.category,
            name="test",
            description="test",
            price=1.00,
            iconId=1,
            isActive=True,
            number=1,
            facts={}
        )
        self.item_id = self.item.id

    def test_restaurant_update(self):
        response = self.client.put(f'/api/v1/item/put/{self.item_id}/', {
            "name": "test",
            "description": "test",
            "price": 1.00,
            "iconId": 1,
            "isActive": True,
            "number": 1,
            "category": 1,
            "facts": {}
        }, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        item = Item.objects.get(id=self.item_id)
        self.assertEqual(item.id, self.item_id)
        self.assertEqual(item.name, 'test')
        self.assertEqual(item.description, 'test')
        self.assertEqual(item.price, 1.00)
        self.assertEqual(item.category.id, self.cat)
        self.assertEqual(item.isActive, True)
        self.assertEqual(item.number, 1)
        self.assertEqual(item.facts, {})

    def test_restaurant_update_bad_request(self):
        response = self.client.put(f'/api/v1/item/put/{self.item_id}/', {
            "name": "test",
            "description": "test",
        }, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_restaurant_update_not_found(self):
        response = self.client.put(f'/api/v1/item/put/100/', {
            "name": "test",
            "description": "test",
            "price": 1.00,
            "iconId": 1,
            "isActive": True,
            "number": 1,
            "facts": {}
        }, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_item_update_no_auth(self):
        response = self.client.put(f'/api/v1/item/put/{self.item_id}/', {
            "name": "test",
            "description": "test",
            "price": 1.00,
            "iconId": 1,
            "isActive": True,
            "number": 1,
            "facts": {}
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ItemUpdateChangeActiveTest(APITestCase):

    def setUp(self):
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
        self.id = self.restaurant.id
        self.category = Category.objects.create(
            name="test",
            number=1,
            isActive=True,
            restaurant=self.restaurant,
            description="test"
        )
        self.cat = self.category.id

        for _ in range(0, 10):
            self.item = Item.objects.create(
                category=self.category,
                name="test",
                description="test",
                price=1.00,
                iconId=1,
                isActive=True,
                number=1,
                facts={}
            )
        self.item_id = self.item.id

    def test_restaurant_update_change_active(self):
        data = {
            "items": [
                {
                    "id": self.item_id,
                    "isActive": False,
                    "category": 1,
                }
            ]
        }
        response = self.client.put(f'/api/v1/item/change-active/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        item = Item.objects.get(id=self.item_id)
        self.assertEqual(item.id, self.item_id)
        self.assertEqual(item.isActive, False)

    def test_restaurant_update_change_active_bad_request(self):
        data = {
            "items": [
                {
                    "id": self.item_id,
                }
            ]
        }
        response = self.client.put(f'/api/v1/item/change-active/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_restaurant_update_change_active_not_found(self):
        data = {
            "items": [
                {
                    "id": 100,
                    "isActive": False
                }
            ]
        }
        response = self.client.put(f'/api/v1/item/change-active/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_item_update_change_active_no_auth(self):
        data = {
            "items": [
                {
                    "id": self.item_id,
                    "isActive": False
                }
            ]
        }
        response = self.client.put(f'/api/v1/item/change-active/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ItemUpdateChangeNumberTest(APITestCase):

    def setUp(self):
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
        self.id = self.restaurant.id
        self.category = Category.objects.create(
            name="test",
            number=1,
            isActive=True,
            restaurant=self.restaurant,
            description="test"
        )
        self.cat = self.category.id
        self.item = Item.objects.create(
            category=self.category,
            name="test",
            description="test",
            price=1.00,
            iconId=1,
            isActive=True,
            number=1,
            facts={}
        )
        self.item_id = self.item.id

    def test_restaurant_update_change_number(self):
        data = {
            "items": [
                {
                    "id": self.item_id,
                    "number": 4,
                    "category": 1,
                }
            ]
        }
        response = self.client.put(f'/api/v1/item/change-number/', data, format='json', HTTP_TOKEN=self.token)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        item = Item.objects.get(id=self.item_id)
        self.assertEqual(item.id, self.item_id)
        self.assertEqual(item.number, 4)

    def test_restaurant_update_change_number_bad_request(self):
        data = {
            "items": [
                {
                    "id": self.item_id,
                }
            ]
        }
        response = self.client.put(f'/api/v1/item/change-number/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_restaurant_update_change_number_not_found(self):
        data = {
            "items": [
                {
                    "id": 100,
                    "number": 4
                }
            ]
        }
        response = self.client.put(f'/api/v1/item/change-number/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)    

    def test_item_update_change_number_no_auth(self):
        data = {
            "items": [
                {
                    "id": self.item_id,
                    "number": 4
                }
            ]
        }
        response = self.client.put(f'/api/v1/item/change-number/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ItemUpdateBulk(APITestCase):

    def setUp(self):
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
        self.id = self.restaurant.id
        self.category = Category.objects.create(
            name="test",
            number=1,
            isActive=True,
            restaurant=self.restaurant,
            description="test"
        )
        self.cat = self.category.id

        for i in range(0, 10):
            self.item = Item.objects.create(
                category=self.category,
                name="test",
                description="test",
                price=1.00,
                iconId=1,
                isActive=True,
                number=1,
                facts={}
            )
        self.item_id = self.item.id

    def test_restaurant_update_bulk(self):
        data = {
            "items": [
                {
                    "id": self.item_id,
                    "name": "test44",
                    "description": "test44",
                    "price": 4.00,
                    "iconId": 11,
                    "isActive": True,
                    "number": 45,
                    "facts": {},
                    "category": 1
                },
                {
                    "id": self.item_id,
                    "name": "test2",
                    "description": "test2",
                    "price": 2.00,
                    "iconId": 4,
                    "isActive": False,
                    "number": 5,
                    "facts": {},
                    "category": 1
                }
            ]
        }
        response = self.client.put(f'/api/v1/item/bulk_update/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        item = Item.objects.get(id=self.item_id)
        self.assertEqual(item.id, self.item_id)
        self.assertEqual(item.name, "test2")

    def test_item_update_bulk_not_auth(self):
        response = self.client.put(f'/api/v1/item/bulk_update/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_item_update_bulk_bad_request(self):
        data = {
            "items": [
                {
                    "id": self.item_id,
                    "name": "test44",
                    "description": "test44",
                    "price": 4.00,
                    "iconId": 'ciao',
                    "isActive": True,
                    "number": 45,
                    "facts": {},
                    "category": 1
                },
                {
                    "id": self.item_id,
                    "name": "test2",
                    "description": "test2",
                    "price": 2.00,
                    "iconId": 4,
                    "isActive": 12,
                    "number": 5,
                    "facts": {},
                    "category": 1
                }
            ]
        }
        response = self.client.put(f'/api/v1/item/bulk_update/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_item_update_bulk_different_categories(self):
        data = {
            "items": [
                {
                    "id": self.item_id,
                    "name": "test44",
                    "description": "test44",
                    "price": 4.00,
                    "iconId": 11,
                    "isActive": True,
                    "number": 45,
                    "facts": {},
                    "category": 1
                },
                {
                    "id": self.item_id,
                    "name": "test2",
                    "description": "test2",
                    "price": 2.00,
                    "iconId": 4,
                    "isActive": False,
                    "number": 5,
                    "facts": {},
                    "category": 2
                }
            ]
        }
        response = self.client.put(f'/api/v1/item/bulk_update/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)