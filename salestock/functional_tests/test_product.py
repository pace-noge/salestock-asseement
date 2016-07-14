from .base import FunctionalTest
from django.core.urlresolvers import reverse
import json
from rest_framework.test import force_authenticate
from rest_framework import status
from products.models import Product



class ProductTest(FunctionalTest):

    def test_get_list_of_product(self):
        self.create_product()
        self.browser.get(self.server_url+"/categories/?format=json")
        self.take_screenshot()
        result = json.loads(self.browser.find_element_by_tag_name("body").text)
        self.assertEqual(result[0]["title"], "test product")
        self.assertEqual(len(result), 1)

    def test_create_product_with_login(self):
        """
        Ensure we can create new product via rest framework client
        """
        url = reverse("product-list")
        data = {
            "title": "second product",
            "slug": "second-product",
            "description": "second product description"
        }
        self.client.force_authenticate(user=self.create_user())
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.get().title, "second product")
        self.browser.get(self.server_url+"/categories/?format=json")
        self.take_screenshot()
        result = json.loads(self.browser.find_element_by_tag_name("body").text)
        self.assertEqual(result[0]["title"], "second product")
        self.assertEqual(len(result), 1)

    def test_create_product_without_login(self):
        url = reverse("product-list")
        data = {
            "title": "second product",
            "slug": "second-product",
            "description": "second product description"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_product(self):
        self.create_product()
        url = reverse("product-detail", kwargs={'slug': 'test-product'})
        data = {
            "title": "second product",
            "description": "second product description"
        }
        self.client.force_authenticate(user=self.create_user())
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(product.objects.get().title, "second product")
        self.browser.get(self.server_url+"/categories/?format=json")
        self.take_screenshot()
        result = json.loads(self.browser.find_element_by_tag_name("body").text)
        self.assertEqual(result[0]["title"], "second product")
        self.assertEqual(len(result), 1)

    def test_delete_product(self):
        self.create_product()
        self.assertEqual(product.objects.count(), 1)
        url = reverse("product-detail", kwargs={'slug': 'test-product'})
        self.client.force_authenticate(user=self.create_user())
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.browser.get(self.server_url+"/categories/?format=json")
        self.take_screenshot()
        result = json.loads(self.browser.find_element_by_tag_name("body").text)
        self.assertEqual(len(result), 0)

    def test_delete_product_without_login(self):
        self.create_product()
        self.assertEqual(product.objects.count(), 1)
        url = reverse("product-detail", kwargs={'slug': 'test-product'})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response.render()
        self.assertEqual(product.objects.count(), 1)
        self.browser.get(self.server_url+"/categories/?format=json")
        self.take_screenshot()
        result = json.loads(self.browser.find_element_by_tag_name("body").text)
        self.assertEqual(len(result), 1)
