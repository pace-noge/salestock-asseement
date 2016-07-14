from django.contrib import admin
from .models import Category, Product
from cms.admin import ContentManageableModelAdmin
# Register your models here.


class ProductAdmin(ContentManageableModelAdmin):
    """
    inherits from ContentManageableModelAdmin, so we didn't describe
    read only fields from models such: created, updated, creator, last_modified_by
    and auto add that fields to metadata at the bottom of admin page.
    """
    list_display = ['title', 'category', 'active']


class Categoryadmin(ContentManageableModelAdmin):
    list_display = ['title', 'active']

admin.site.register(Category, Categoryadmin)
admin.site.register(Product, ProductAdmin)