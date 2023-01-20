from rest_framework.test import APITestCase
from rest_framework import status

from restaurant.models import Restaurant, Item, Category
from order.models import Order, Take
from accounts.models import RestaurantUser


class TakesUpdateTest(APITestCase):

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

        self.order = Order.objects.create(
            restaurant=self.restaurant,
            payment_method="test",
            payment_status="test",
            order_status="test",
            note="test",
        )

        self.order_id = self.order.id
        take = Take.objects.create(
            order=self.order,
            item=self.item,
            quantity=1,
            batch=1,
        ) 
        self.take_id = take.id

    def test_udpate_take(self):
        data = {
            'quantity': 2,
            'batch': 2,
            'order': self.order_id,
            'item': self.itemId,
        }
        response = self.client.put(f'/api/v1/take/put/{self.take_id}/',data,  format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        res = response.json()

        self.assertEqual(res.get('quantity'), 2)
        self.assertEqual(res.get('batch'), 2)
        self.assertEqual(res.get('order'), self.order_id)
        self.assertEqual(res.get('item'), self.itemId)

    def test_update_take_with_invalid_data(self):
        data = {
            'quantity': 2,
            'batch': 2,
        }
        response = self.client.put(f'/api/v1/take/put/{self.take_id}/',data,  format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_take_no_auth(self):
        response = self.client.put(f'/api/v1/take/put/{self.take_id}/',  format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)