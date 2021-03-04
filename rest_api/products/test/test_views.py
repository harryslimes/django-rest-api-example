from django.urls import reverse
from django.contrib.auth.hashers import check_password
from nose.tools import ok_, eq_
from rest_framework.test import APITestCase
from rest_framework import status
from faker import Faker
import random
from decimal import Decimal
import factory
from ..models import Product
from .factories import ProductFactory

fake = Faker()


class TestProductListTestCase(APITestCase):
    """
    Tests /products list operations.
    """

    def setUp(self):
        self.url = reverse('product-list')
        self.product_data = factory.build(dict, FACTORY_CLASS=ProductFactory)
        
    def test_post_request_with_no_data_fails(self):
        response = self.client.post(self.url, {})
        eq_(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_request_with_valid_data_succeeds(self):
        response = self.client.post(self.url, self.product_data)
        eq_(response.status_code, status.HTTP_201_CREATED)

        product = Product.objects.get(pk=response.data.get('id'))
        eq_(product.sku, self.product_data.get('sku'))

class TestProductDetailTestCase(APITestCase):
    """
    Tests /products detail operations.
    """

    def setUp(self):
        self.product = ProductFactory()
        self.url = reverse('product-detail', kwargs={'sku': self.product.sku})

    def test_get_request_returns_a_given_user(self):
        response = self.client.get(self.url)
        eq_(response.status_code, status.HTTP_200_OK)

    def test_put_request_updates_a_user(self):
        new_price = round(random.uniform(0.00, 9999.99),2)
        payload = {'price': new_price}
        response = self.client.patch(self.url, payload)
        eq_(response.status_code, status.HTTP_200_OK)

        product = Product.objects.get(pk=self.product.id)
        eq_(product.price, round(Decimal(new_price),2))
