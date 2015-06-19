# coding=utf-8

from django.db import models

from taggit.managers import TaggableManager

class Food(models.Model):
    title = models.CharField(max_length=255)
    tags = TaggableManager()
    def __unicode__(self):
        return self.title
