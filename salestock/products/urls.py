# from .views import CategoryListView, CategoryDetailView, CategoryViewSet, ProductViewSet
from . import views
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns


product_list = views.ProductViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
product_detail = views.ProductViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

product_list_by_category  = views.ProductCategoryList.as_view()


urlpatterns = [
    url(r'^$', product_list, name="product-list"),
    url(r'^(?P<slug>[-\w]+)/$', product_detail, name="product-detail"),
    url(r'^category/(?P<slug>[-\w]+)/$', product_list_by_category, name='product-category-list'),

]

urlpatterns = format_suffix_patterns(urlpatterns)