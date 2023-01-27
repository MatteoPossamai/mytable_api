from rest_framework.test import APITestCase
from rest_framework import status

from restaurant.models import Restaurant, Item, Category
from order.models import Order, Take
from accounts.models import RestaurantUser


class TakesCreateTest(APITestCase):

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

        self.order = Order.objects.create(
            restaurant=self.restaurant,
            payment_method="test",
            payment_status="test",
            order_status="test",
            note="test",
        )
        self.order.save()
        self.order_id = self.order.id

    def test_create_take(self):
        data = {
            'order': self.order_id,
            'item': self.itemId,
            'quantity': 1,
            'batch': 1
        }
        response = self.client.post('/api/v1/take/create/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get('order'), self.order_id)
        self.assertEqual(response.json().get('item'), self.itemId)
        self.assertEqual(response.json().get('quantity'), 1)

    def test_create_take_with_invalid_order(self):
        data = {
            'order': 100,
            'item': self.itemId,
        }
        response = self.client.post('/api/v1/take/create/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

