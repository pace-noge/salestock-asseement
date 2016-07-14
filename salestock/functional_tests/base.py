from datetime import datetime
import os
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from products.models import Category, Product
from rest_framework import status
from rest_framework.test import APILiveServerTestCase
from selenium import webdriver


SCREEN_DUMP_LOCATION = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'screendumps'
)

SERVER_URL = "http://localhost:8000"

class FunctionalTest(APILiveServerTestCase):

    def setUp(self):
        if not os.path.exists(SCREEN_DUMP_LOCATION):
            os.makedirs(SCREEN_DUMP_LOCATION)
        self.server_url = SERVER_URL
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)
        self.Category = Category
        self.Product = Product

    def tearDown(self):
        self.browser.quit()
        super(FunctionalTest, self).tearDown()

    def take_screenshot(self):
        file_name = self._get_file_name() + '.png'
        print 'Screenshooting to %s' % file_name
        self.browser.get_screenshot_as_file(file_name)

    def _get_file_name(self):
        timestamp = datetime.now().isoformat().replace(":", "_")[:19]
        return '{folder}/{classname}.{method}-{timestamp}'.format(
            folder=SCREEN_DUMP_LOCATION,
            classname=self.__class__.__name__,
            method=self._testMethodName,
            timestamp=timestamp
        )

    def create_category(self):
        return Category.objects.create(
            title="test category",
            slug="test-category",
            description="Description for test category"
        )

    def create_product(self):
        category = self.create_category()
        product = Product.objects.create(
            title="Test Product",
            slug="test-product",
            size="M",
            color="Black",
            price=199000,
            category=category)
        return product

    def create_user(self):
        user = User.objects.create_user(
            username="testuser",
            email="mail@mail.com",
            password="topsecret")
        return user