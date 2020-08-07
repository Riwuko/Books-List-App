from django.db import models
from django.contrib.postgres.fields import ArrayField

class Book(models.Model):
    title = models.CharField(max_length=200)
    authors = ArrayField(models.CharField(max_length=200))
    published_date = models.DateField()
    categories = ArrayField(models.CharField(max_length=200,blank=True, null=True),null=True,blank=True)
    average_rating = models.FloatField(blank=True, null=True)
    rating_count = models.FloatField(blank=True, null=True)
    thumbnail = models.URLField(blank=True, null=True)

    def __str__(self):
        return f'title: {self.title}, authors: {self.authors}'
    
    class Meta:
        unique_together = ('title', 'authors')