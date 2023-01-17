from rest_framework.test import APITestCase
from rest_framework import status

from restaurant.models.restaurant import Restaurant
from accounts.models import RestaurantUser


class OrderCreateTestCase(APITestCase):

    def setUp(self):
        self.user = RestaurantUser.objects.create(
            username="test",
            email="test@test.com",
            password="password123",
        )
        self.restaurant = Restaurant.objects.create(
            name="test",
            plan={},
            location="test",
            phone="test",
            owner=self.user,
        )
        self.identificator = self.restaurant.id

    def test_order_create(self):
        data = {
            "restaurant": self.identificator,
            
        }
        response = self.client.post('/api/v1/order/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        print(response.json())