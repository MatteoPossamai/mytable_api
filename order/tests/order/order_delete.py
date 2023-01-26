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

        obj = Order.objects.create(
                restaurant=self.restaurant,
                payment_method="test",
                payment_status="test",
                order_status="test",
                note="test",
            )

        self.order_id = obj.id

    def test_order_delete(self):
        response = self.client.delete(f'/api/v1/order/delete/{self.order_id}/', format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Order.objects.count(), 0)

    def test_order_delete_not_existing(self):
        response = self.client.delete(f'/api/v1/order/delete/999/', format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_order_delete_not_owner(self):
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
        self.obj_id = obj.id

        response = self.client.delete(f'/api/v1/order/delete/{self.obj_id}/', format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_order_delete_no_auth(self):
        response = self.client.delete(f'/api/v1/order/delete/{self.order_id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DeleteAllTest(APITestCase):
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
        self.user.is_staff = True
        self.user.save()

        self.data = {
            'username': 'test123',
            'email': 'test@test.com',
            'password': 'password123'
        }
        response = self.client.post('/api/v1/restaurant_user/signup/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.token2 = response.json().get('token')

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

    def test_delete_all(self):
        response = self.client.delete(f'/api/v1/order/delete/', format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Order.objects.count(), 0)

    def test_delete_all_no_auth_user(self):
        response = self.client.delete(f'/api/v1/order/delete/', format='json', HTTP_TOKEN=self.token2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)