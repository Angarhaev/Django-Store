import re

from django.contrib.auth.models import User, Permission
from django.test import TestCase

from shopapp.models import Product, Order
from shopapp.utils import add_two_numbers
from string import ascii_letters
from random import choices
from django.shortcuts import reverse


class AddTwoNumbers(TestCase):
    def test_add_two_numbers(self):
        res = add_two_numbers(4, 5)
        self.assertEqual(res, 9)


class OrderDetailViewTestCase(TestCase):
    username, password, user = [None for _ in range(3)]

    @classmethod
    def setUpClass(cls):
        cls.username = 'test_user_' + ''.join(choices(ascii_letters, k=10))
        cls.password = ''.join(choices(ascii_letters, k=10))
        cls.user = User.objects.create_user(username=cls.username, password=cls.password)
        permission = Permission.objects.get(codename='view_order')
        cls.user.user_permissions.add(permission)
        cls.user.save()

    @classmethod
    def tearDownClass(cls):
        if cls.user:
            cls.user.delete()

    def setUp(self) -> None:
        self.client.login(username=self.username, password=self.password)

    def tearDown(self) -> None:
        self.client.logout()

    def test_is_create_user(self):
        self.assertIsNotNone(self.user)

    def test_view_order(self):
        response = self.client.get(reverse('shopapp:orders_list'), HTTP_USER_AGENT='test-agent')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Orders")


class OrderCreateTestCase(TestCase):
    username, password, user, order, product, name = [None for _ in range(6)]
    delivery_address = 'test_address_' + ''.join(choices(ascii_letters, k=10))
    promocode = 'test_promo_' + ''.join(choices(ascii_letters, k=5))

    @classmethod
    def setUpClass(cls):
        cls.username = 'test_user_' + ''.join(choices(ascii_letters, k=10))
        cls.password = ''.join(choices(ascii_letters, k=10))
        cls.user = User.objects.create_user(username=cls.username, password=cls.password)
        permission = Permission.objects.get(codename='view_order')

        cls.user.user_permissions.add(permission)
        cls.user.save()

    @classmethod
    def tearDownClass(cls):
        if cls.user:
            cls.user.delete()

    def setUp(self) -> None:
        self.client.login(username=self.username, password=self.password)
        self.name = 'test_product_' + ''.join(choices(ascii_letters, k=10))
        self.product = Product.objects.create(name=self.name, created_by=self.user)
        self.order = Order.objects.create(delivery_address=self.delivery_address,
                                          promocode=self.promocode,
                                          user=self.user)
        self.order.products.add(self.product)

    def tearDown(self) -> None:
        self.order.delete()
        self.client.logout()

    def test_order_details(self):
        order_pk = None
        response = self.client.get(reverse('shopapp:order_detail', kwargs={'pk': self.order.pk}),
                                   HTTP_USER_AGENT='test-agent')

        self.assertContains(response, self.delivery_address)
        self.assertContains(response, self.promocode)
        self.assertContains(response, self.product.name)

        pattern = r'Order #(\d+)'
        string = response.content.decode()
        match = re.search(pattern=pattern, string=string)
        if match:
            order_pk = int(match.group(1))

        self.assertEqual(self.order.pk, order_pk)


class OrderExportTestCase(TestCase):
    fixtures = ['orders-fixture.json', 'products-fixture.json', 'users-fixture.json', 'groups-fixture.json']

    username, password, user = [None for _ in range(3)]

    def setUp(self) -> None:
        self.username = 'test_user_' + ''.join(choices(ascii_letters, k=10))
        self.password = ''.join(choices(ascii_letters, k=10))
        self.user = User.objects.create_user(username=self.username, password=self.password, is_staff=True)
        delivery_address = 'test_address_' + ''.join(choices(ascii_letters, k=10))
        promocode = 'test_promo_' + ''.join(choices(ascii_letters, k=5))
        self.client.login(username=self.username, password=self.password)
        self.order = Order.objects.create(delivery_address=delivery_address,
                                          promocode=promocode,
                                          user=self.user)
        #print(Product.objects.all())
        for pk in range(1, 4):
            self.product = Product.objects.get(pk=pk)
            self.order.products.add(self.product)

    def tearDown(self) -> None:
        self.order.delete()
        self.client.logout()
        if self.user:
            self.user.delete()


    def test_get_order_json(self):
        response = self.client.get(reverse('shopapp:order_export'), HTTP_USER_AGENT='test-agent')
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.order_by("pk").all()
        expected_data = [
            {
                'pk': order.pk,
                'deliver_address': order.delivery_address,
                'promocode': order.promocode,
                'created_at': str(order.created_at),
                'user': order.user.username,
                'products': list(order.products.order_by('pk').all().values_list('name', flat=True))
             }
            for order in orders
        ]
        orders_data = response.json()
        print(orders_data)
        self.assertEqual(orders_data['orders'], expected_data,)
