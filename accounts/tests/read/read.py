from rest_framework.test import APITestCase
from rest_framework import status

from accounts.models.restaurant_user import RestaurantUser

class RestaurantUserRead(APITestCase):

    def test_read_all_zero(self):
        response = self.client.get('/api/v1/restaurant_user/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

    def test_read_all_one(self):
        RestaurantUser.objects.create(
            username='test',
            password='password11',
            email='ciao@gmail.com'
        )

        response = self.client.get('/api/v1/restaurant_user/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0].get('username'), 'test')

    def test_read_ten_success(self):
        for i in range(10):
            RestaurantUser.objects.create(
                username='test' + str(i),
                password='password11',
                email='ciao@gmail.com' + str(i)
            )
        response = self.client.get('/api/v1/restaurant_user/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 10)
        self.assertEqual(response.json()[0].get('username'), 'test0')

    def test_read_one(self):
        RestaurantUser.objects.create(
            username='test',
            password='password11',
            email='ciao@gmail.com'
        )
        response = self.client.get('/api/v1/restaurant_user/get/ciao@gmail.com/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('username'), 'test')

    def test_read_one_not_ind_db(self):
        response = self.client.get('/api/v1/restaurant_user/get/ciao@gmail.com/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json().get('error'), 'User not found')       
