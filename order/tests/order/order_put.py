from rest_framework.test import APITestCase
from rest_framework import status

from restaurant.models import Restaurant, Item, Category
from order.models import Order, Take
from accounts.models import RestaurantUser


class OrderPutTestCase(APITestCase):

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

        self.cat = Category.objects.create(
            name="test",
            restaurant=self.restaurant,
            number=1,
        )

        self.item = Item.objects.create(
            name="test",
            price=1.0,
            description="test",
            category=self.cat,
            iconId=1,
            isActive=True,
            number=1,
            facts={},
        )
        self.item.save()
        self.itemId = self.item.id