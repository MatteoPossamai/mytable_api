from rest_framework.test import APITestCase
from rest_framework import status
from django.core.cache import cache

from restaurant.models.category import Category
from restaurant.models.restaurant import Restaurant
from accounts.models import RestaurantUser

class CategoryDeleteTest(APITestCase):

    def tearDown(self):
        cache.clear()
        Category.objects.all().delete()
        Restaurant.objects.all().delete()
        RestaurantUser.objects.all().delete()

    def setUp(self):
        cache.clear()
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
            name="test1",
            location="test",
            phone="test",
            owner=self.user,
        )
        self.id = self.restaurant.id
        Category.objects.create(
            name="test",
            number=1,
            isActive=True,
            restaurant=self.restaurant,
            description="test"
        )

    def test_restaurant_delete(self):
        category = Category.objects.get(name="test")
        identifier = category.id
        response = self.client.delete(f'/api/v1/category/delete/{identifier}/', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)

    def test_restaurant_delete_multiple(self):
        number_of_categories = 10
        for i in range(number_of_categories):
            Category.objects.create(
                name=f"test{i}",
                number=1,
                isActive=True,
                restaurant=self.restaurant,
                description="test"
            )

        for i in range(number_of_categories):
            category = Category.objects.get(name=f"test{i}")
            identifier = category.id
            response = self.client.delete(f'/api/v1/category/delete/{identifier}/', HTTP_TOKEN=self.token)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(Category.objects.count(), number_of_categories-i)

    def test_restaurant_delete_no_id(self):
        response = self.client.delete('/api/v1/category/delete/', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_restaurant_delete_wrong_id(self):
        response = self.client.delete('/api/v1/category/delete/999/', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_restaurant_delete_no_token(self):
        category = Category.objects.get(name="test")
        identifier = category.id
        response = self.client.delete(f'/api/v1/category/delete/{identifier}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)