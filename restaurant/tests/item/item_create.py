from rest_framework.test import APITestCase
from rest_framework import status

from restaurant.models.category import Category
from restaurant.models.item import Item
from restaurant.models.restaurant import Restaurant
from accounts.models import RestaurantUser

class ItemCreateTest(APITestCase):

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
        self.identificator = self.restaurant.id

        self.category = Category.objects.create(
            name="test",
            number=1, 
            isActive=True,
            restaurant=self.restaurant,
            description="test"
        )
        self.cat = self.category.id

    def test_restaurant_create(self):
        data = {
            "restaurant": self.identificator,
            "category": self.cat,
            "name": "test",
            "description": "test",
            "price": 1.00,
            "iconId": 1,
            "isActive": True,
            "number": 1,
            "facts": {}
        }
        response = self.client.post('/api/v1/item/create/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.get().name, 'test')

    def test_restaurant_create_missing(self):
        data = {
            "restaurant": self.identificator,
            "category": self.cat,
            "name": "test",
            "facts": {}
        }
        response = self.client.post('/api/v1/item/create/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Item.objects.count(), 0)

    def test_create_category_no_auth(self):
        response = self.client.post('/api/v1/item/create/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Item.objects.count(), 0)
