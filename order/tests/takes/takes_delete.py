from rest_framework.test import APITestCase
from rest_framework import status

from restaurant.models import Restaurant, Item, Category
from order.models import Order, Take
from accounts.models import RestaurantUser


class TakesDeleteTest(APITestCase):

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
        for i in range(10):
            take = Take.objects.create(
                order=self.order,
                item=self.item,
                quantity=1,
                batch=1,
            ) 
            self.take_id = take.id

    def test_takes_delete(self):
        response = self.client.delete(f'/api/v1/take/delete/{self.take_id}/', format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Take.objects.count(), 9)

    def test_takes_delete_no_auth(self):
        response = self.client.delete(f'/api/v1/take/delete/{self.take_id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_takes_delete_by_restaurant(self):
        response = self.client.delete(f'/api/v1/take/delete/restaurant/{self.identificator}/', format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Take.objects.count(), 0)

    def test_takes_delete_by_restaurant_no_auth(self):
        response = self.client.delete(f'/api/v1/take/delete/restaurant/{self.identificator}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_takes_delete_not_existing_restaurant(self):
        response = self.client.delete(f'/api/v1/take/delete/restaurant/11100/', format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_takes_delete_by_order(self):
        response = self.client.delete(f'/api/v1/take/delete/order/{self.order_id}/', format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Take.objects.count(), 0)

    def test_takes_delete_by_order_no_auth(self):
        response = self.client.delete(f'/api/v1/take/delete/order/{self.order_id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_takes_delete_not_existing_order(self):
        response = self.client.delete(f'/api/v1/take/delete/order/121300/', format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)