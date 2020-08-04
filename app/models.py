from django.db import models

class Book(models.Model):
    id = models.CharField(primary_key=True)
    title = models.CharField()
    authors = ArrayField(models.CharField()
    published_date = models.DateField()
    categories = ArrayField(models.CharField()
    average_rating = models.IntegerField()
    rating_count = models.FloatField()
    thumbnail = models.URLField()

    def __str__(self):
        return f'title: {self.title}, authors: {self.authors}'