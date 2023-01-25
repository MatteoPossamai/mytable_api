from rest_framework.test import APITestCase
from rest_framework import status

from restaurant.models.restaurant import Restaurant
from accounts.models import RestaurantUser


class TestDeleteProducts(APITestCase):

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

    def test_get_products(self):
        response = self.client.post('/api/v1/stripe/delete-subscription/', format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)