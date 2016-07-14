from .models import Category, Product
from rest_framework import serializers
from django.template.defaultfilters import slugify



class CategorySerializer(serializers.ModelSerializer):
    """
    Return serializers of category models
    """
    products = serializers.HyperlinkedIdentityField(view_name='product-category-list', lookup_field='slug')


    class Meta:
        model = Category
        fields = ('title', 'slug', 'products', 'description', 'active')


    def create(self, validated_data):
        """
        if slug is empty then populate with slugify based on title
        """
        if 'slug' not in validated_data or not validated_data['slug']:
            validated_data['slug'] = slugify(validated_data['title'])
        return Category.objects.create(**validated_data)


class ProductSerializer(serializers.ModelSerializer):
    """
    return serializers for Product models
    """
    detail_url = serializers.HyperlinkedIdentityField(view_name='product-detail', lookup_field='slug')

    class Meta:
        model = Product
        fields = ('title', 'slug', 'category', 'size', 'color', 'price', 'active', 'detail_url')
        extra_kwargs = {'url': {'lookup_field': 'slug'}}
