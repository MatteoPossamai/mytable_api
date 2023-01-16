from rest_framework.test import APITestCase
from rest_framework import status
from django.core.cache import cache

from restaurant.models.category import Category
from restaurant.models.item import Item
from restaurant.models.restaurant import Restaurant
from accounts.models.restaurant_user import RestaurantUser

class ItemReadSingleTest(APITestCase):

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
        self.id = self.restaurant.id
        self.category = Category.objects.create(
            name="test",
            number=1,
            isActive=True,
            restaurant=self.restaurant,
            description="test"
        )
        self.cat = self.category.id
        self.item = Item.objects.create(
            category=self.category,
            name="test",
            description="test",
            price=1.00,
            iconId=1,
            isActive=True,
            number=1,
            facts={}
        )
        self.item_id = self.item.id

    def test_restaurant_read(self):
        response = self.client.get(f'/api/v1/item/{self.item_id}/', HTTP_TOKEN=self.token)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['id'], self.item_id)
        self.assertEqual(data['name'], 'test')
        self.assertEqual(data['description'], 'test')
        self.assertEqual(data['price'], '1.00')
        self.assertEqual(data['iconId'], 1)
        self.assertEqual(data['isActive'], True)
        self.assertEqual(data['number'], 1)
        self.assertEqual(data['facts'], {})

    def test_restaurant_read_no_id(self):
        response = self.client.get('/api/v1/item/0/', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_restaurant_read_wrong_id(self):
        response = self.client.get('/api/v1/item/read/999/', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_item_read_no_auth(self):
        response = self.client.get(f'/api/v1/item/{self.item_id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ItemReadItemMultiple(APITestCase):

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
        self.id = self.restaurant.id
        self.category = Category.objects.create(
            name="test",
            number=1,
            isActive=True,
            restaurant=self.restaurant,
            description="test"
        )
        self.cat = self.category.id
        self.num = 10

        for i in range(self.num):
            self.item = Item.objects.create(
                category=self.category,
                name="test" + str(i),
                description="test",
                price=1.00,
                iconId=1,
                isActive=True,
                number=1,
                facts={}
            )

    def test_restaurant_read(self):
        response = self.client.get('/api/v1/item/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.num)
        self.assertEqual(response.data[0]['name'], 'test0')
        self.assertEqual(response.data[0]['description'], 'test')
        self.assertEqual(response.data[0]['price'], '1.00')
        self.assertEqual(response.data[0]['iconId'], 1)
        self.assertEqual(response.data[0]['isActive'], True)
        self.assertEqual(response.data[0]['number'], 1)
        self.assertEqual(response.data[0]['facts'], {})
        self.assertEqual(len(response.data), self.num)


class ItemReadByRestaurant(APITestCase):

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
            name="test",
            plan={},
            location="test",
            phone="test",
            owner=self.user,
        )
        self.id = self.restaurant.id
        self.category = Category.objects.create(
            name="test",
            number=1,
            isActive=True,
            restaurant=self.restaurant,
            description="test"
        )
        self.cat = self.category.id
        self.item = Item.objects.create(
            category=self.category,
            name="test",
            description="test",
            price=1.00,
            iconId=1,
            isActive=True,
            number=1,
            facts={}
        )

        self.res2 = Restaurant.objects.create(
            name="test2",
            plan={},
            location="test",
            phone="test",
            owner=self.user,
        )

        self.cat2 = Category.objects.create(
            name="test2",
            number=1,
            isActive=True,
            restaurant=self.res2,
            description="test"
        )

        self.item2 = Item.objects.create(
            category=self.cat2,
            name="test",
            description="test",
            price=1.00,
            iconId=1,
            isActive=True,
            number=1,
            facts={}
        )
        self.item_id = self.item.id

    def test_restaurant_read(self):
        response = self.client.get(f'/api/v1/item/restaurant_item/{self.id}/', HTTP_TOKEN=self.token)

        data = response.json().get('items')
        self.assertEqual(len(data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0]['id'], self.item_id)
        self.assertEqual(data[0]['name'], 'test')
        self.assertEqual(data[0]['description'], 'test')
        self.assertEqual(data[0]['price'], '1.00')
        self.assertEqual(data[0]['iconId'], 1)
        self.assertEqual(data[0]['isActive'], True)
        self.assertEqual(data[0]['number'], 1)
        self.assertEqual(data[0]['facts'], {})

        data = {
            "category": self.cat,
            "name": "test23",
            "description": "test23",
            "price": 1.00,
            "iconId": 1,
            "isActive": True,
            "number": 1,
            "facts": {}
        }

        response = self.client.post('/api/v1/item/create/', data, format='json', HTTP_TOKEN=self.token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(f'/api/v1/item/restaurant_item/{self.id}/', HTTP_TOKEN=self.token)
        data = response.json().get('items')
        self.assertEqual(len(data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0]['id'], self.item_id)
        self.assertEqual(data[0]['name'], 'test')
        self.assertEqual(data[0]['description'], 'test')
        self.assertEqual(data[0]['price'], '1.00')
        self.assertEqual(data[0]['iconId'], 1)
        self.assertEqual(data[0]['isActive'], True)
        self.assertEqual(data[0]['number'], 1)
        self.assertEqual(data[0]['facts'], {})

    def test_restaurant_read_no_auth(self):
        response = self.client.get(f'/api/v1/item/restaurant_item/{self.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ItemReadByRestaurantActive(APITestCase):

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
            name="test",
            plan={},
            location="test",
            phone="test",
            owner=self.user,
        )
        self.id = self.restaurant.id
        self.category = Category.objects.create(
            name="test",
            number=1,
            isActive=True,
            restaurant=self.restaurant,
            description="test"
        )
        self.cat = self.category.id
        for i in range(10):
            self.item = Item.objects.create(
                category=self.category,
                name="test",
                description="test",
                price=1.00,
                iconId=1,
                isActive=True if i % 2 == 0 else False,
                number=1,
                facts={}
            )

        self.item_id = self.item.id

    def test_restaurant_read_active_items(self):
        response = self.client.get(f'/api/v1/item/restaurant_item/active/{self.id}/', HTTP_TOKEN=self.token)

        data = response.json().get('items')
        self.assertEqual(len(data), 5)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0]['name'], 'test')
        self.assertEqual(data[0]['description'], 'test')
        self.assertEqual(data[0]['price'], '1.00')
        self.assertEqual(data[0]['iconId'], 1)
        self.assertEqual(data[0]['isActive'], True)
        self.assertEqual(data[0]['number'], 1)
        self.assertEqual(data[0]['facts'], {})

    def test_restaurant_read_active_items_no_auth(self):
        response = self.client.get(f'/api/v1/item/restaurant_item/active/{self.id}/', HTTP_TOKEN="123")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ItemReadByCategory(APITestCase):

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
            name="test",
            plan={},
            location="test",
            phone="test",
            owner=self.user,
        )
        self.id = self.restaurant.id
        self.category = Category.objects.create(
            name="test",
            number=1,
            isActive=True,
            restaurant=self.restaurant,
            description="test"
        )
        self.cat = self.category.id
        for i in range(10):
            self.item = Item.objects.create(
                category=self.category,
                name="test",
                description="test",
                price=1.00,
                iconId=1,
                isActive=True if i % 2 == 0 else False,
                number=1,
                facts={}
            )

        self.item_id = self.item.id

        self.category2 = Category.objects.create(
            name="test2",
            number=12,
            isActive=True,
            restaurant=self.restaurant,
            description="test"
        )
        self.cat2 = self.category2.id
        for i in range(4):
            self.item = Item.objects.create(
                category=self.category2,
                name="test",
                description="test",
                price=1.00,
                iconId=1,
                isActive=True if i % 2 == 0 else False,
                number=1,
                facts={}
            )

        self.item_id = self.item.id

    def test_restaurant_read_category_items(self):
        response = self.client.get(f'/api/v1/item/category_item/{self.cat}/', HTTP_TOKEN=self.token)

        data = response.json().get('items')
        self.assertEqual(len(data), 10)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0]['name'], 'test')
        self.assertEqual(data[0]['description'], 'test')
        self.assertEqual(data[0]['price'], '1.00')
        self.assertEqual(data[0]['iconId'], 1)
        self.assertEqual(data[0]['isActive'], True)
        self.assertEqual(data[0]['number'], 1)
        self.assertEqual(data[0]['facts'], {})

        response = self.client.get(f'/api/v1/item/category_item/{self.cat2}/', HTTP_TOKEN=self.token)

        data = response.json().get('items')
        self.assertEqual(len(data), 4)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0]['name'], 'test')
        self.assertEqual(data[0]['description'], 'test')
        self.assertEqual(data[0]['price'], '1.00')
        self.assertEqual(data[0]['iconId'], 1)
        self.assertEqual(data[0]['isActive'], True)
        self.assertEqual(data[0]['number'], 1)
        self.assertEqual(data[0]['facts'], {})

    def test_restaurant_read_category_items_no_auth(self):
        response = self.client.get(f'/api/v1/item/category_item/{self.cat}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ItemReadByCategoryActive(APITestCase):

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
            name="test",
            plan={},
            location="test",
            phone="test",
            owner=self.user,
        )
        self.id = self.restaurant.id
        self.category = Category.objects.create(
            name="test",
            number=1,
            isActive=True,
            restaurant=self.restaurant,
            description="test"
        )
        self.cat = self.category.id
        for i in range(10):
            self.item = Item.objects.create(
                category=self.category,
                name="test",
                description="test",
                price=1.00,
                iconId=1,
                isActive=True if i % 2 == 0 else False,
                number=1,
                facts={}
            )

        self.item_id = self.item.id

        self.category2 = Category.objects.create(
            name="test2",
            number=12,
            isActive=True,
            restaurant=self.restaurant,
            description="test"
        )
        self.cat2 = self.category2.id
        for i in range(4):
            self.item = Item.objects.create(
                category=self.category2,
                name="test",
                description="test",
                price=1.00,
                iconId=1,
                isActive=True if i % 2 == 0 else False,
                number=1,
                facts={}
            )

        self.item_id = self.item.id

    def test_restaurant_read_category_items(self):
        response = self.client.get(f'/api/v1/item/category_item/active/{self.cat}/', HTTP_TOKEN=self.token)

        data = response.json().get('items')
        self.assertEqual(len(data), 5)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0]['name'], 'test')
        self.assertEqual(data[0]['description'], 'test')
        self.assertEqual(data[0]['price'], '1.00')
        self.assertEqual(data[0]['iconId'], 1)
        self.assertEqual(data[0]['isActive'], True)
        self.assertEqual(data[0]['number'], 1)
        self.assertEqual(data[0]['facts'], {})

        response = self.client.get(f'/api/v1/item/category_item/active/{self.cat2}/', HTTP_TOKEN=self.token)

        data = response.json().get('items')
        self.assertEqual(len(data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0]['name'], 'test')
        self.assertEqual(data[0]['description'], 'test')
        self.assertEqual(data[0]['price'], '1.00')
        self.assertEqual(data[0]['iconId'], 1)
        self.assertEqual(data[0]['isActive'], True)
        self.assertEqual(data[0]['number'], 1)
        self.assertEqual(data[0]['facts'], {})

    def test_restaurant_read_category_items_no_auth(self):
        response = self.client.get(f'/api/v1/item/category_item/active/{self.cat}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)