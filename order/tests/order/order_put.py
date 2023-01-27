from rest_framework.test import APITestCase
from rest_framework import status

from restaurant.models import Restaurant, Item, Category
from order.models import Order
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

    def test_put_order(self):
        data = {
            "payment_method": "cash",
            "payment_status": "paid",
            "order_status": "pending",
            "note": "test123",
            "restaurant": self.identificator,
        }
        response = self.client.put(f'/api/v1/order/put/{self.order_id}/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data.get('payment_method'), "cash")
        self.assertEqual(data.get('payment_status'), "paid")
        self.assertEqual(data.get('order_status'), "pending")
        self.assertEqual(data.get('note'), "test123")


    def test_put_order_not_logged(self):
        response = self.client.put(f'/api/v1/order/put/{self.order_id}/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_order_data_uncomplete(self):
        data = {
            "payment_method": "cash",
            "payment_status": "paid",
            "order_status": "pending",
            "note": "test123",
        }
        response = self.client.put(f'/api/v1/order/put/{self.order_id}/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class OrderPutChangeStatus(APITestCase):

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

    def test_order_put_change_status(self):
        data = {
            "order_status": "pending",
        }
        response = self.client.put(f'/api/v1/order/update/status/{self.order_id}/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data.get('order_status'), "pending")

    def test_order_put_change_status_not_logged(self):
        response = self.client.put(f'/api/v1/order/update/status/{self.order_id}/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_order_put_change_status_data_uncomplete(self):
        response = self.client.put(f'/api/v1/order/update/status/{self.order_id}/', {}, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class OrderPutChangePaymentStatus(APITestCase):

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

    def test_order_put_change_payment_status(self):
        data = {
            "payment_status": "paid",
        }
        response = self.client.put(f'/api/v1/order/update/payment_status/{self.order_id}/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data.get('payment_status'), "paid")

    def test_order_put_change_payment_status_not_logged(self):
        response = self.client.put(f'/api/v1/order/update/payment_status/{self.order_id}/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_order_put_change_payment_status_data_uncomplete(self):
        response = self.client.put(f'/api/v1/order/update/payment_status/{self.order_id}/', {}, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)