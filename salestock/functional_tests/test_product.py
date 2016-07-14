from .base import FunctionalTest
from django.core.urlresolvers import reverse
import json
from rest_framework.test import force_authenticate
from rest_framework import status
from products.models import Product, Category



class ProductTest(FunctionalTest):

    # get product list
    def test_get_list_of_product(self):
        self.create_product()
        self.browser.get(self.server_url+"/products/?format=json")
        self.take_screenshot()
        result = json.loads(self.browser.find_element_by_tag_name("body").text)
        self.assertEqual(result[0]["title"], "Test Product")
        self.assertEqual(len(result), 1)

    # create new product with valid login
    def test_create_product_with_login(self):
        """
        Ensure we can create new product via rest framework client
        """
        url = reverse("product-list")
        data = {
            "title": "second product",
            "size": "M",
            "color": "Black",
            "price": 190000,
            "category": self.create_category().id
        }
        self.client.force_authenticate(user=self.create_user())
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.get().title, "second product")
        self.browser.get(self.server_url+"/products/?format=json")
        self.take_screenshot()
        result = json.loads(self.browser.find_element_by_tag_name("body").text)
        self.assertEqual(result[0]["title"], "second product")
        self.assertEqual(len(result), 1)

    # trying to create product without login
    def test_create_product_without_login(self):
        url = reverse("product-list")
        data = {
            "title": "second product",
            "size": "M",
            "color": "Black",
            "price": 190000,
            "category": self.create_category().id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.browser.get(self.server_url+"/products/?format=json")
        self.take_screenshot()
        result = json.loads(self.browser.find_element_by_tag_name("body").text)
        self.assertEqual(len(result), 0)

    # update product
    def test_update_product(self):
        self.create_product()
        url = reverse("product-detail", kwargs={'slug': 'test-product'})
        data = {
            "title": "second product",
            "size": "M",
            "color": "Black",
            "price": 190000,
            "category": Category.objects.get().id
        }
        self.client.force_authenticate(user=self.create_user())
        response = self.client.put(url, data, format='json')
        print response.content
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.get().title, "second product")
        self.browser.get(self.server_url+"/products/?format=json")
        self.take_screenshot()
        result = json.loads(self.browser.find_element_by_tag_name("body").text)
        self.assertEqual(result[0]["title"], "second product")
        self.assertEqual(len(result), 1)


    # create multiple product for filtering later
    def create_multi_product(self):
        category1 = Category.objects.create(
            title="category 1",
            description="Category Satu")
        category2 = Category.objects.create(
            title="Category 2",
            description="Category dua"
        )

        Product.objects.create(
            title="product1",
            size="M",
            color="Black",
            price=750000,
            category=category1)
        Product.objects.create(
            title="product2",
            size="S",
            color="Red",
            price=500000,
            category=category1)
        Product.objects.create(
            title="product3",
            size="M",
            color="Black",
            price=750000,
            category=category2)


    # filter product with same category
    def test_filter_product_based_on_same_category(self):
        self.create_multi_product()
        self.browser.get(self.server_url+"/products/category/category-1/?format=json")
        self.take_screenshot()
        result = json.loads(self.browser.find_element_by_tag_name("body").text)
        self.assertEqual(result[0]["title"], "product1")
        self.assertEqual(result[1]["title"], "product2")
        self.assertEqual(len(result), 2)

    # filter product based on size
    def test_filter_product_based_on_size(self):
        self.create_multi_product()
        self.browser.get(self.server_url+"/products/?format=json&size=M")
        self.take_screenshot()
        result = json.loads(self.browser.find_element_by_tag_name("body").text)
        self.assertEqual(result[0]["title"], "product1")
        self.assertEqual(result[1]["title"], "product3")
        self.assertEqual(len(result), 2)

    # filter product based on category and size
    def test_filter_product_based_on_category_and_size(self):
        self.create_multi_product()
        self.browser.get(self.server_url+"/products/category/category-1/?format=json&size=M")
        self.take_screenshot()
        result = json.loads(self.browser.find_element_by_tag_name("body").text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "product1")

    # filter product based on color
    def test_filter_product_based_on_color(self):
        self.create_multi_product()
        self.browser.get(self.server_url+"/products/?format=json&color=Black")
        self.take_screenshot()
        result = json.loads(self.browser.find_element_by_tag_name("body").text)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["title"], "product1")
        self.assertEqual(result[1]["title"], "product3")

    # filter product based on price


    # def test_delete_product(self):
    #     self.create_product()
    #     self.assertEqual(product.objects.count(), 1)
    #     url = reverse("product-detail", kwargs={'slug': 'test-product'})
    #     self.client.force_authenticate(user=self.create_user())
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.browser.get(self.server_url+"/categories/?format=json")
    #     self.take_screenshot()
    #     result = json.loads(self.browser.find_element_by_tag_name("body").text)
    #     self.assertEqual(len(result), 0)

    # def test_delete_product_without_login(self):
    #     self.create_product()
    #     self.assertEqual(product.objects.count(), 1)
    #     url = reverse("product-detail", kwargs={'slug': 'test-product'})
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #     response.render()
    #     self.assertEqual(product.objects.count(), 1)
    #     self.browser.get(self.server_url+"/categories/?format=json")
    #     self.take_screenshot()
    #     result = json.loads(self.browser.find_element_by_tag_name("body").text)
    #     self.assertEqual(len(result), 1)
