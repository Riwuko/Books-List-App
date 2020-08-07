from django.db.models import Q
from django.http import JsonResponse
from django_filters  import rest_framework as filters

import json
import requests

from app.models import Book

class BookFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    authors = filters.CharFilter(lookup_expr='icontains')
    categories = filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Book
        fields = ('title','authors','categories')


def download_items(arg):
    request = f'https://www.googleapis.com/books/v1/volumes?q={arg}'
    downloaded_books = requests.get(request).json()['items']
    return downloaded_books

def find_books_for_update(books):
    q=Q()
    for book in books:
        q |= Q(title=book['title'], authors=book['authors'],published_date=book['published_date'])
        
    filtered_books = Book.objects.filter(q)

    for book in books:
        for filtered in filtered_books:
            if filtered.title == book['title'] and filtered.authors == book['authors']:
                filtered.categories = book['categories']
                filtered.average_rating = book['average_rating']
                filtered.rating_count = book['rating_count']
                filtered.thumbnail = book['thumbnail']
    
    return filtered_books

def prepare_items(items):
    prepared_items = [{
        
            'title':item["volumeInfo"].get("title"),
            'authors':item["volumeInfo"].get("authors"),
            'published_date':item["volumeInfo"].get("publishedDate") if len(item["volumeInfo"].get("publishedDate"))==10 else f'{item["volumeInfo"].get("publishedDate")}-01-01',
            'categories':item['volumeInfo'].get('categories') if item['volumeInfo'].get('categories') else None,
            'average_rating':item["volumeInfo"].get("averageRating"),
            'rating_count':item["volumeInfo"].get("ratingsCount"),
            'thumbnail':item["volumeInfo"]["imageLinks"].get("thumbnail")
        }
         for item in items ]
    return prepared_items