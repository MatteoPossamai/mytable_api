from rest_framework.test import APITestCase
from rest_framework import status

from restaurant.models.restaurant import Restaurant
from accounts.models import RestaurantUser
from order.models.order import Order


class OrderReadAllTestCase(APITestCase):

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

    def test_order_read_all_zero(self):
        response = self.client.get('/api/v1/order/', format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.json()), 0)
        self.assertEqual(Order.objects.count(), 0)

    def test_order_read_all_one(self):
        Order.objects.create(
            restaurant=self.restaurant,
            payment_method="test",
            payment_status="test",
            order_status="test",
            note="test",
        )

        response = self.client.get('/api/v1/order/', format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0].get('restaurant'), self.identificator)
        self.assertEqual(response.json()[0].get('payment_method'), "test")
        self.assertEqual(response.json()[0].get('payment_status'), "test")
        self.assertEqual(response.json()[0].get('order_status'), "test")
        self.assertEqual(response.json()[0].get('note'), "test")

        self.assertEqual(Order.objects.count(), 1)

    def test_order_read_all_ten(self):
        for i in range(10):
            Order.objects.create(
                restaurant=self.restaurant,
                payment_method="test",
                payment_status="test",
                order_status="test",
                note="test",
            )

        response = self.client.get('/api/v1/order/', format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.json()), 10)
        self.assertEqual(response.json()[0].get('restaurant'), self.identificator)
        self.assertEqual(response.json()[0].get('payment_method'), "test")
        self.assertEqual(response.json()[0].get('payment_status'), "test")
        self.assertEqual(response.json()[0].get('order_status'), "test")
        self.assertEqual(response.json()[0].get('note'), "test")

        self.assertEqual(Order.objects.count(), 10)

        
class OrderReadOneTestCase(APITestCase):

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

        obj = Order.objects.create(
            restaurant=self.restaurant,
            payment_method="test",
            payment_status="test",
            order_status="test",
            note="test",
        )

        self.order_id = obj.id

    def test_read_one_order(self):
        response = self.client.get(f'/api/v1/order/{self.order_id}/', format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json().get('restaurant'), self.identificator)
        self.assertEqual(response.json().get('payment_method'), "test")
        self.assertEqual(response.json().get('payment_status'), "test")
        self.assertEqual(response.json().get('order_status'), "test")
        self.assertEqual(response.json().get('note'), "test")

        self.assertEqual(Order.objects.count(), 1)

    def test_read_one_order_not_found(self):
        response = self.client.get(f'/api/v1/order/9999999999/', format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Order.objects.count(), 1)

    def test_read_one_order_no_auth(self):
        response = self.client.get(f'/api/v1/order/{self.order_id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(Order.objects.count(), 1)

    def test_read_one_order_not_mine(self):
        self.data = {
            'username': 'test123',
            'email': 'test@test.com',
            'password': 'password123'
        }
        response = self.client.post('/api/v1/restaurant_user/signup/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.user1 = RestaurantUser.objects.get(username='test123')

        self.restaurant1 = Restaurant.objects.create(
            name="test2",
            location="test",
            phone="test",
            owner=self.user1,
        )

        obj = Order.objects.create(
            restaurant=self.restaurant1,
            payment_method="test",
            payment_status="test",
            order_status="test",
            note="test",
        )

        self.order_id = obj.id

        response = self.client.get(f'/api/v1/order/{self.order_id}/', format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
