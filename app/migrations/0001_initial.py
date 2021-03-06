# Generated by Django 2.2.15 on 2020-08-09 16:19

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                (
                    "author",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=200), size=None
                    ),
                ),
                ("published_date", models.DateField(null=True)),
                (
                    "categories",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(blank=True, max_length=200, null=True),
                        blank=True,
                        null=True,
                        size=None,
                    ),
                ),
                ("average_rating", models.FloatField(blank=True, null=True)),
                ("rating_count", models.FloatField(blank=True, null=True)),
                ("thumbnail", models.URLField(blank=True, null=True)),
            ],
            options={"unique_together": {("title", "author")},},
        ),
    ]
