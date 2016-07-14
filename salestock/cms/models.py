from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Create your models here.
class ContentManageable(models.Model):
    """
    All models inherits from this models to automatically add created, creator
    updated, last_modified_by fields to models
    """
    created = models.DateTimeField(default=timezone.now, blank=True, db_index=True)
    updated = models.DateTimeField(blank=True)
    creator = models.ForeignKey(User, null=True, blank=True, related_name="%(app_label)s_%(class)s_creator")
    last_modified_by = models.ForeignKey(User, null=True, blank=True, related_name="%(app_label)s_%(class)s_modified")

    """
    set updated fields with current time
    """
    def save(self, **kwargs):
        self.updated = timezone.now()
        return super(ContentManageable, self).save(**kwargs)


    class Meta:
        """
        Abstract true, so django didn't create table for this models
        """
        abstract = True