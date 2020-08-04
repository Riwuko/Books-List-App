from django.db import models
from django.contrib.postgres.fields import ArrayField

class Book(models.Model):
    id = models.CharField(max_length=200,primary_key=True)
    title = models.CharField(max_length=200)
    authors = ArrayField(models.CharField(max_length=200))
    published_date = models.DateField()
    categories = ArrayField(models.CharField(max_length=200,blank=True))
    average_rating = models.IntegerField()
    rating_count = models.IntegerField()
    thumbnail = models.URLField()

    def __str__(self):
        return f'title: {self.title}, authors: {self.authors}'