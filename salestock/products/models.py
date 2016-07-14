from __future__ import unicode_literals

from django.db import models
from cms.models import ContentManageable
from django.template.defaultfilters import slugify
# Create your models here.


class Category(ContentManageable):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, null=True, unique=True)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)


    def __unicode__(self):
        return self.title


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Category, self).save(*args, **kwargs)

    class Meta:
        """
        verbose name on django admin page
        """
        verbose_name_plural = "categories"


class ProductQuerySet(models.query.QuerySet):
    # return currently active products
    def active(self):
        return self.filter(active=True)


class ProductManager(models.Manager):

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    # override django filter.all so the returned data only with active=True
    def all(self, *args, **kwargs):
        return self.get_queryset().active()


    def filter_by_category(self, category_slug):
        return self.get_queryset().filter(category__slug=category_slug)



class Product(ContentManageable):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, null=True, unique=True)
    category = models.ForeignKey(Category, related_name='products')
    size = models.CharField(max_length=4)
    color = models.CharField(max_length=120)
    price = models.DecimalField(decimal_places=0, max_digits=10)
    active = models.BooleanField(default=True)
    objects = ProductManager()

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Product, self).save(*args, **kwargs)
