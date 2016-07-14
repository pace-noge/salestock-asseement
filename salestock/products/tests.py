from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, APIClient, force_authenticate
from .models import Category, Product

from .views import CategoryViewSet, ProductViewSet
# Create your tests here.
from django.contrib.auth.models import AnonymousUser, User
import json


class CategoriesPageTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_categories_root_url_resolvers_to_category_viewset_view(self):
        category = Category.objects.create(
            title='test category',
            slug= 'test-category',
            description="test description"
        )
        view = CategoryViewSet.as_view({'get': 'list'})
        request = self.factory.get(reverse('category-list'))
        response = view(request)
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertIn("test category", response.content)


    def test_categories_get_category_by_slug_resolve_to_category_viewset(self):
        category = Category.objects.create(
            title='test category',
            slug= 'test-category',
            description="test description"
        )
        view = CategoryViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(
            reverse(
                'category-detail',
                kwargs={'slug': 'test-category'}
            )
        )
        response = view(request, slug='test-category')
        response.render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('"slug":"test-category"', response.content)


    def test_create_categories_resolve_to_category_viewset_without_login(self):
        data = {
            'title': 'create category',
            'slug': 'create-category',
            'description': 'test create category'
        }
        url = reverse('category-list')
        view = CategoryViewSet.as_view({'post': 'create'})
        request = self.factory.post(url, data, format='json')
        response = view(request)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            '{"detail":"Authentication credentials were not provided."}',
            response.content
        )

    def test_create_categories_resolve_to_category_viewset_with_login(self):
        user = User.objects.create_user(username="nasa", email="mail@mail.com", password="topsecret")
        data = {
            'title': 'create category',
            'slug': 'create-category',
            'description': 'test create category'
        }
        url = reverse('category-list')
        view = CategoryViewSet.as_view({'post': 'create'})
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=user)
        response = view(request)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get().title, 'create category')

    def test_create_categories_by_models_django_orm(self):
        category = Category.objects.create(
            title="test category",
            slug="test-category",
            description="description of category"
        )
        result = Category.objects.get()
        self.assertEqual(result.title, "test category")
        self.assertEqual(result.slug, "test-category")
        self.assertEqual(Category.objects.count(), 1)

    def test_delete_category_by_slug_resolve_by_viewset_without_login(self):
        category = Category.objects.create(
            title="test category",
            slug="test-category",
            description="description of category"
        )
        url = reverse(
            "category-detail",
            kwargs={'slug': 'test-category'}
        )
        view = CategoryViewSet.as_view(
            {
                'delete': 'destroy',
            }
        )
        request = self.factory.delete(url)
        response = view(request, slug='test-category')
        response.render()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Category.objects.count(), 1)

    def test_delete_category_by_slug_resolve_by_viewset_with_login(self):
        user = User.objects.create_user(username="nasa", email="mail@mail.com", password="topsecret")
        category = Category.objects.create(
            title="test category",
            slug="test-category",
            description="description of category"
        )
        url = reverse(
            "category-detail",
            kwargs={'slug': 'test-category'}
        )
        view = CategoryViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete(url)
        force_authenticate(request, user=user)
        response = view(request, slug='test-category')
        response.render()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)


class ProductsPageTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()


    # django ORM test (models)

    def test_create_product_by_orm(self):
        category = Category.objects.create(
            title="test category",
            slug="test-category",
            description="description of category"
        )
        product = Product.objects.create(
            title="test product",
            size="M",
            color="Black",
            category=category,
            price=199000
        )

        result = Product.objects.get()
        self.assertEqual(result.title, "test product")
        self.assertEqual(result.category, category)

    def test_product_object_manager_filter_by_category(self):
        category = Category.objects.create(
            title="test category",
            slug="test-category",
            description="description of category"
        )
        product = Product.objects.create(
            title="test product",
            size="M",
            color="Black",
            category=category,
            price=199000
        )
        result = Product.objects.filter_by_category("test-category")[0]
        self.assertEqual(result.title, "test product")
        self.assertEqual(result.category, category)
        self.assertEqual(Product.objects.count(), 1)

    def test_get_all_query_only_return_active_products(self):
        category = Category.objects.create(
            title="test category",
            slug="test-category",
            description="description of category"
        )
        Product.objects.create(
            title="test product",
            size="M",
            color="Black",
            category=category,
            price=199000
        )
        Product.objects.create(
            title="test product 2",
            size="M",
            color="Black",
            category=category,
            price=199000,
            active=False
        )
        result = Product.objects.all()
        self.assertEqual(result.count(), 1)
        self.assertEqual(result[0].title, "test product")

    def test_delete_product_via_orm(self):
        category = Category.objects.create(
            title="test category",
            slug="test-category",
            description="description of category"
        )
        Product.objects.create(
            title="test product",
            slug='test-product',
            size="M",
            color="Black",
            category=category,
            price=199000
        )

        result = Product.objects.get(slug='test-product')
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(result.title, "test product")
        self.assertEqual(result.category, category)
        result.delete()
        self.assertEqual(Product.objects.count(), 0)


    # test for mapping url to viewset

    def test_create_product_resolve_by_viewset_without_login(self):
        category = Category.objects.create(
            title="test category",
            slug="test-category",
            description="description of category"
        )
        data = {
            "title":"test product",
            "slug":'test-product',
            "size":"M",
            "color":"Black",
            "category": 1,
            "price":199000
        }

        url = reverse("product-list")
        view = ProductViewSet.as_view(
            {
                'post': 'create',
            }
        )
        request = self.factory.post(url, data, format='json')
        response = view(request)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Product.objects.count(), 0)

    def test_create_product_resolve_by_viewset_with_login(self):
        user = User.objects.create_user(username="nasa", email="mail@mail.com", password="topsecret")
        category = Category.objects.create(
            title="test category",
            slug="test-category",
            description="description of category"
        )
        data = {
            "title":"test product",
            "slug":'test-product',
            "size":"M",
            "color":"Black",
            "category": 1,
            "price":199000
        }

        url = reverse("product-list")
        view = ProductViewSet.as_view(
            {
                'post': 'create',
            }
        )
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=user)
        response = view(request)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        p = Product.objects.get(slug='test-product')
        self.assertEqual(p.title, "test product")
        self.assertEqual(p.category, category)
        self.assertEqual(p.creator, user)

    def test_list_all_active_product_by_viewset(self):
        category = Category.objects.create(
            title="test category",
            slug="test-category",
            description="description of category"
        )
        Product.objects.create(
            title="test product",
            size="M",
            color="Black",
            category=category,
            price=199000
        )
        Product.objects.create(
            title="test product 2",
            size="M",
            color="Black",
            category=category,
            price=199000,
            active=False
        )

        url = reverse("product-list")
        request = self.factory.get(url)
        view = ProductViewSet.as_view({'get': 'list'})
        response = view(request)
        response.render()
        json_data = json.loads(response.content)
        self.assertEqual(len(json_data), 1)
        self.assertEqual(json_data[0]['title'], "test product")
        self.assertEqual(int(json_data[0]['price']), 199000)
        self.assertEqual(Product.objects.count(), 2)

    def test_update_product_by_viewset_without_login(self):
        category = Category.objects.create(
            title="test category",
            slug="test-category",
            description="description of category"
        )
        Product.objects.create(
            title="test product",
            slug="test-category",
            size="M",
            color="Black",
            category=category,
            price=199000
        )
        data = {
            "title": "test product update"
        }
        url = reverse("product-detail", kwargs={'slug': "test-product"})
        request = self.factory.put(url, data, format='json')
        view = ProductViewSet.as_view({'put': "update"})
        response = view(request)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(Product.objects.get().title, "test product update")

    def test_update_product_by_viewset_with_login(self):
        user = User.objects.create_user(
            username="nasa",
            email="mail@mail.com",
            password="topsecret"
        )
        category = Category.objects.create(
            title="test category",
            slug="test-category",
            description="description of category"
        )
        Product.objects.create(
            title="test product",
            slug="test-product",
            size="M",
            color="Black",
            category=category,
            price=199000
        )
        data = {
            "title": "test product update",
            "slug": "test-product",
            "size": "S",
            "color": "Red",
            "category": 1,
            "price": 169000
        }
        url = reverse("product-detail", kwargs={'slug': "test-product"})
        request = self.factory.put(url, data, format='json')
        force_authenticate(request, user=user)
        view = ProductViewSet.as_view({'put': "update"})
        response = view(request, slug="test-product")
        response.render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.get().title, "test product update")
        self.assertEqual(Product.objects.count(), 1)

    def test_delete_product_by_viewset_without_login(self):
        category = Category.objects.create(
            title="test category",
            slug="test-category",
            description="description of category"
        )
        Product.objects.create(
            title="test product",
            slug="test-category",
            size="M",
            color="Black",
            category=category,
            price=199000
        )
        url = reverse("product-detail", kwargs={'slug': "test-product"})
        request = self.factory.delete(url)
        view = ProductViewSet.as_view({'delete': "destroy"})
        response = view(request)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(Product.objects.count(), 0)

    def test_delete_product_by_viewset_with_login(self):
        user = User.objects.create_user(
            username="nasa",
            email="mail@mail.com",
            password="topsecret"
        )
        category = Category.objects.create(
            title="test category",
            slug="test-category",
            description="description of category"
        )
        Product.objects.create(
            title="test product",
            slug="test-product",
            size="M",
            color="Black",
            category=category,
            price=199000
        )
        url = reverse("product-detail", kwargs={'slug': "test-product"})
        request = self.factory.delete(url)
        force_authenticate(request, user=user)
        view = ProductViewSet.as_view({'delete': "destroy"})
        response = view(request, slug="test-product")
        response.render()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)





