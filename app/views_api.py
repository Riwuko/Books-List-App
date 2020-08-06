import json
from django.http import JsonResponse
import requests

from app.models import Book

def download_items(arg):
    request = f'https://www.googleapis.com/books/v1/volumes?q={arg}'
    downloaded_books = requests.get(request).json()['items']
    return downloaded_books

def prepare_items(items):
    return (
        [
            item["volumeInfo"]["title"],
            item["volumeInfo"]["authors"],
            item["volumeInfo"]["publishedDate"],
            item['volumeInfo'].get('categories'),
            item["volumeInfo"].get("averageRating"),
            item["volumeInfo"].get("ratingsCount"),
            item["volumeInfo"]["imageLinks"]["thumbnail"]
        ] for item in items )

    

    
# def prepare_items(items):
#     prepared_books = []
#         [
#             prepared_books.push(
#                 title=item["volumeInfo"]["title"],
#                 authors=item["volumeInfo"]["authors"],
#                 published_date=item["volumeInfo"]["publishedDate"],
#                 categories = item["volumeInfo"]["categories"],
#                 average_rating = item["volumeInfo"]["averageRating"],
#                 ratings_count = item["volumeInfo"]["ratingsCount"],
#                 thumbnail = item["volumeInfo"]["imageLinks"]["thumbnail"]
#                 )
#             for item in items
#         ]
#     )

