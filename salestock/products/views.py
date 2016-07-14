from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
import django_filters
from rest_framework import generics, viewsets, filters




class CategoryViewSet(viewsets.ModelViewSet):
    """
    Viewset for categories
    """
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductFilter(filters.FilterSet):
    """
    Filter class for filtering product based on: color, size, min_price, max_price
    """
    min_price = django_filters.NumberFilter(name='price', lookup_type='gte')
    max_price = django_filters.NumberFilter(name='price', lookup_type='lte')
    color = django_filters.CharFilter(name='color', lookup_type='icontains')

    class Meta:
        model = Product
        fields = ('color', 'size', 'min_price', 'max_price')


class ProductViewSet(viewsets.ModelViewSet):
    """
    Return REST action for products
    """
    lookup_field = 'slug'
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ProductFilter

    """
    Auto populate the creator field with current user that create the product
    """
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    """
    Auto populate current user who perform update
    """
    def perform_update(self, serializer):
        serializer.save(last_modified_by=self.request.user)



class ProductCategoryList(generics.ListAPIView):
    """
    return the product filtered from url kwargs:
    url:
        http://localhost/products/category/<slug>
    """
    serializer_class = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ProductFilter

    def get_queryset(self):
        category_slug = self.kwargs['slug']
        return Product.objects.filter_by_category(category_slug)
