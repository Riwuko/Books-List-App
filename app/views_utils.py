from django.db.models import Q
from itertools import chain

import requests

from app.models import Book


def download_items(arg):
    request_url = "https://www.googleapis.com/books/v1/volumes"
    return requests.get(request_url, params={"q": arg}).json().get("items")


def find_books_for_update(books):
    q = Q()
    for book in books:
        q |= Q(title=book["title"], author=book["author"], published_date=book["published_date"])

    filtered_books = Book.objects.filter(q)
    for book in books:
        for filtered in filtered_books:
            if filtered.title == book["title"] and filtered.author == book["author"]:
                filtered.categories = book["categories"]
                filtered.average_rating = book["average_rating"]
                filtered.rating_count = book["rating_count"]
                filtered.thumbnail = book["thumbnail"]

    return filtered_books


def get_proper_date(published_date):
    if not published_date:
        return None
    defaults = ["01", "01"]
    published_date = published_date.split("-")
    year, month, day, *_ = chain(published_date, defaults)
    return f"{year}-{month}-{day}"


def prepare_items(items):
    return [
        {
            "title": item["volumeInfo"].get("title"),
            "author": item["volumeInfo"].get("authors", ["UNKNOWN"]),
            "published_date": get_proper_date(item["volumeInfo"].get("publishedDate")),
            "categories": item["volumeInfo"].get("categories"),
            "average_rating": item["volumeInfo"].get("averageRating"),
            "rating_count": item["volumeInfo"].get("ratingsCount"),
            "thumbnail": item["volumeInfo"].get("imageLinks", {}).get("thumbnail"),
        }
        for item in items
    ]
