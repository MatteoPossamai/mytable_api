from rest_framework.test import APITestCase
from rest_framework import status

from restaurant.models import Restaurant, Item, Category
from order.models import Order, Take
from accounts.models import RestaurantUser


class OrderCreateTestCase(APITestCase):

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

    def test_order_create(self):
        data = {
            "restaurant_id": self.identificator,
            "payment_method": "test",
            "payment_status": "test",
            "order_status": "test",
            "note": "test",
            "items": [
                {   
                    "id": self.itemId,
                    "quantity": 1,
                },
            ],
            
        }
        response = self.client.post('/api/v1/order/create/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()

        self.assertEqual(data.get('restaurant'), self.identificator)
        self.assertEqual(data.get('payment_method'), "test")
        self.assertEqual(data.get('payment_status'), "test")
        self.assertEqual(data.get('order_status'), "pending")
        self.assertEqual(data.get('note'), "test")

        self.assertEqual(Take.objects.count(), 1)

    def test_order_create_bad_request(self):
        data = {
            "restaurant_id": 23,
            "payment_method": "test",
            "payment_status": "test",
            "order_status": "test",
            "note": "test",
            "items": [
                {   
                    "id": self.itemId,
                    "quantity": 1,
                },
            ],
            
        }
        response = self.client.post('/api/v1/order/create/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = response.json()

        self.assertEqual(data.get('error'), 'Bad request')

    def test_order_create_no_auth(self):
        response = self.client.post('/api/v1/order/create/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)