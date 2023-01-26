from rest_framework.test import APITestCase
from rest_framework import status

from restaurant.models import Restaurant, Item, Category
from order.models import Order, Take
from accounts.models import RestaurantUser


class TakesGetTest(APITestCase):

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

        self.order_id = self.order.id
        for i in range(10):
            take = Take.objects.create(
                order=self.order,
                item=self.item,
                quantity=1,
                batch=1,
            ) 
            self.take_id = take.id

    def test_get_all_takes(self):
        response = self.client.get(f'/api/v1/take/', format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.json()), 10)

    def test_get_all_take_no_auth(self):
        response = self.client.get(f'/api/v1/take/', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_take(self):
        response = self.client.get(f'/api/v1/take/get/{self.take_id}/', format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('id'), self.take_id)
        self.assertEqual(response.json().get('order'), self.order_id)
        self.assertEqual(response.json().get('item'), self.itemId)
        self.assertEqual(response.json().get('quantity'), 1)
        self.assertEqual(response.json().get('batch'), 1)

    def test_get_take_no_auth(self):
        response = self.client.get(f'/api/v1/take/get/{self.take_id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_take_not_found(self):
        response = self.client.get(f'/api/v1/take/get/100/', format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_takes_by_order(self):
        response = self.client.get(f'/api/v1/take/get/order/{self.order_id}/', format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.json()), 10)

    def test_get_takes_by_order_empty(self):
        res = Restaurant.objects.create(
            name="test123",
            location="test",
            phone="test",
            owner=self.user,
        )
        response = self.client.get(f'/api/v1/take/get/order/{res.id}/', format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.json()), 0)

    def get_takes_by_order_no_auth(self):
        response = self.client.get(f'/api/v1/take/get/order/{self.order_id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
