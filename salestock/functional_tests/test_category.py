from .base import FunctionalTest
from django.core.urlresolvers import reverse
import json
from rest_framework.test import force_authenticate
from rest_framework import status
from products.models import Category



class CategoryTest(FunctionalTest):

    def test_get_list_of_category(self):
        self.create_category()
        self.browser.get(self.server_url+"/categories/?format=json")
        self.take_screenshot()
        result = json.loads(self.browser.find_element_by_tag_name("body").text)
        self.assertEqual(result[0]["title"], "test category")
        self.assertEqual(len(result), 1)

    def test_create_category_with_login(self):
        """
        Ensure we can create new category via rest framework client
        """
        url = reverse("category-list")
        data = {
            "title": "second category",
            "slug": "second-category",
            "description": "second category description"
        }
        self.client.force_authenticate(user=self.create_user())
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.get().title, "second category")
        self.browser.get(self.server_url+"/categories/?format=json")
        self.take_screenshot()
        result = json.loads(self.browser.find_element_by_tag_name("body").text)
        self.assertEqual(result[0]["title"], "second category")
        self.assertEqual(len(result), 1)

    def test_create_category_without_login(self):
        url = reverse("category-list")
        data = {
            "title": "second category",
            "slug": "second-category",
            "description": "second category description"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_category(self):
        self.create_category()
        url = reverse("category-detail", kwargs={'slug': 'test-category'})
        data = {
            "title": "second category",
            "description": "second category description"
        }
        self.client.force_authenticate(user=self.create_user())
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.get().title, "second category")
        self.browser.get(self.server_url+"/categories/?format=json")
        self.take_screenshot()
        result = json.loads(self.browser.find_element_by_tag_name("body").text)
        self.assertEqual(result[0]["title"], "second category")
        self.assertEqual(len(result), 1)

    def test_delete_category(self):
        self.create_category()
        self.assertEqual(Category.objects.count(), 1)
        url = reverse("category-detail", kwargs={'slug': 'test-category'})
        self.client.force_authenticate(user=self.create_user())
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.browser.get(self.server_url+"/categories/?format=json")
        self.take_screenshot()
        result = json.loads(self.browser.find_element_by_tag_name("body").text)
        self.assertEqual(len(result), 0)

    def test_delete_category_without_login(self):
        self.create_category()
        self.assertEqual(Category.objects.count(), 1)
        url = reverse("category-detail", kwargs={'slug': 'test-category'})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response.render()
        self.assertEqual(Category.objects.count(), 1)
        self.browser.get(self.server_url+"/categories/?format=json")
        self.take_screenshot()
        result = json.loads(self.browser.find_element_by_tag_name("body").text)
        self.assertEqual(len(result), 1)
