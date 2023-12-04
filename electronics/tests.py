from datetime import datetime
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from electronics.models import NetworkNode, Product
from users.models import User


class NetworkNodeTestCase(APITestCase):

    def setUp(self):
        user = User.objects.create(
            email='admin@admin.ru',
            first_name='Admin',
            last_name='Adminov',
            role='admin',
        )

        user.set_password('123456')
        user.save()

        self.networknode = NetworkNode.objects.create(
            name="TestNode",
            email="email@email.com",
            country="Russia",
            city="Moscow",
            street="Pushkina",
            house_number="111",
            node_type="factory",
        )
        response = self.client.post('/users/login/', {'email': 'admin@admin.ru', 'password': '123456'})
        token = response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_get_list(self):
        """ Test for getting list of network nodes """

        self.maxDiff = None

        response = self.client.get(
            reverse('electronics:networknode_view_list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        current_time = timezone.now().replace(second=0, microsecond=0).strftime('%Y-%m-%dT%H:%M:%S') + 'Z'

        response_json = response.json()

        response_json['results'][0]['creation_time'] = timezone.datetime.strptime(
            response_json['results'][0]['creation_time'],
            '%Y-%m-%dT%H:%M:%S.%fZ'
        ).replace(second=0, microsecond=0).strftime('%Y-%m-%dT%H:%M:%S') + 'Z'

        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.networknode.id,
                        "name": "TestNode",
                        "email": "email@email.com",
                        "country": "Russia",
                        "city": "Moscow",
                        "street": "Pushkina",
                        "house_number": 111,
                        "creation_time": current_time,
                        "debt": "0.00",
                        "hierarchy_level": 0,
                        "node_type": "factory",
                        "supplier": None,
                        "products": []
                    },
                ]
            }
        )

    def test_create_node(self):
        """ Test for creating a network node """

        data = {
            "name": "NewNode",
            "email": "new@email.com",
            "country": "USA",
            "city": "New York",
            "street": "Broadway",
            "house_number": 123,
            "node_type": "ie",
            "supplier": self.networknode.id
        }

        response = self.client.post(
            reverse('electronics:networknode_create'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NetworkNode.objects.count(), 2)

    def test_retrieve_node(self):
        """ Test for retrieving a network node """

        response = self.client.get(
            reverse('electronics:networknode_view', args=[self.networknode.id])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                "id": self.networknode.id,
                "name": "TestNode",
                "email": "email@email.com",
                "country": "Russia",
                "city": "Moscow",
                "street": "Pushkina",
                "house_number": 111,
                "creation_time": response.json()['creation_time'],
                "debt": "0.00",
                "hierarchy_level": 0,
                "node_type": "factory",
                "supplier": None,
                "products": []
            }
        )

    def test_update_node(self):
        """ Test for updating a network node """

        data = {
            "name": "UpdatedNode",
            "email": "updated@email.com",
            "country": "Germany",
            "city": "Berlin",
            "street": "Brandenburger",
            "house_number": 999,
            "node_type": "factory",
        }

        response = self.client.put(
            reverse('electronics:networknode_update', args=[self.networknode.id]),
            data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.networknode.refresh_from_db()
        self.assertEqual(self.networknode.name, "UpdatedNode")
        self.assertEqual(self.networknode.country, "Germany")

    def test_delete_node(self):
        """ Test for deleting a network node """

        response = self.client.delete(
            reverse('electronics:networknode_delete', args=[self.networknode.id])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(NetworkNode.objects.count(), 0)  # Assuming there was one node created in setUp


class ProductTestCase(APITestCase):

    def setUp(self):
        user = User.objects.create(
            email='admin@admin.ru',
            first_name='Admin',
            last_name='Adminov',
            role='admin',
        )

        user.set_password('123456')
        user.save()

        self.networknode = NetworkNode.objects.create(
            name="TestNode",
            email="email@email.com",
            country="Russia",
            city="Moscow",
            street="Pushkina",
            house_number="111",
            node_type="factory",
        )

        self.product = Product.objects.create(
            name="TestProduct",
            model="XYZ",
            release_date="2023-12-01",
            supplier=self.networknode,
        )

        response = self.client.post('/users/login/', {'email': 'admin@admin.ru', 'password': '123456'})
        token = response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_list_products(self):
        """ Test for listing all products """

        another_product = Product.objects.create(
            name="AnotherProduct",
            model="123",
            release_date="2023-12-10",
            supplier=self.networknode,
        )

        response = self.client.get(
            reverse('electronics:product_view_list')
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.product.id,
                        "name": "TestProduct",
                        "model": "XYZ",
                        "release_date": "2023-12-01",
                        "supplier": self.networknode.id,
                    },
                    {
                        "id": another_product.id,
                        "name": "AnotherProduct",
                        "model": "123",
                        "release_date": "2023-12-10",
                        "supplier": self.networknode.id,
                    },
                ]
            }
        )

    def test_create_product(self):
        """ Test for creating a product """

        data = {
            "name": "NewProduct",
            "model": "ABC",
            "release_date": "2023-12-15",
            "supplier": self.networknode.id,
        }

        response = self.client.post(
            reverse('electronics:product_create'),
            data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_retrieve_product(self):
        """ Test for retrieving a product """

        response = self.client.get(
            reverse('electronics:product_view', args=[self.product.id])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "id": self.product.id,
                "name": "TestProduct",
                "model": "XYZ",
                "release_date": "2023-12-01",
                "supplier": self.networknode.id,
            }
        )

    def test_update_product(self):
        """ Test for updating a product """

        data = {
            "name": "UpdatedProduct",
            "model": "DEF",
            "release_date": "2023-12-20",
            "supplier": self.networknode.id,
        }

        response = self.client.put(
            reverse('electronics:product_update', args=[self.product.id]),
            data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()

        expected_date = datetime.strptime(data["release_date"], "%Y-%m-%d").date()

        self.assertEqual(self.product.name, "UpdatedProduct")
        self.assertEqual(self.product.release_date, expected_date)

    def test_delete_product(self):
        """ Test for deleting a product """

        response = self.client.delete(
            reverse('electronics:product_delete', args=[self.product.id])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)
