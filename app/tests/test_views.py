from django.db.models import Q
from django.test import Client, TestCase
from django.urls import reverse
from unittest.mock import Mock, patch

from app.models import Book
from app.tests.tests_utils import GoogleBookResponse


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.add_url = reverse("db")
        self.list_url = reverse("book-list")
        self.id = 1
        self.detail_url = reverse("book-detail", args=[str(self.id)])

        Book.objects.create(
            pk=self.id, title="book", authors=["author"], published_date="1999-01-01"
        )

    def test_book_list_GET_positive(self):
        response = self.client.get(self.list_url)
        expected_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.id,
                    "title": "book",
                    "authors": ["author"],
                    "published_date": "1999-01-01",
                    "categories": None,
                    "average_rating": None,
                    "rating_count": None,
                    "thumbnail": None,
                }
            ],
        }

        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding="utf8"), expected_response)

    def test_book_list_GET_negative(self):
        response = self.client.get(self.list_url)

        expected_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.id,
                    "title": "book",
                    "authors": ["author"],
                    "published_date": "1999-01-02",
                    "categories": None,
                    "average_rating": None,
                    "rating_count": None,
                    "thumbnail": None,
                }
            ],
        }

        self.assertEquals(response.status_code, 200)
        self.assertJSONNotEqual(str(response.content, encoding="utf8"), expected_response)

    def test_book_detail_GET(self):
        response = self.client.get(self.detail_url)
        expected_response = {
            "id": 1,
            "title": "book",
            "authors": ["author"],
            "published_date": "1999-01-01",
            "categories": None,
            "average_rating": None,
            "rating_count": None,
            "thumbnail": None,
        }

        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding="utf8"), expected_response)

    def test_book_add_POST_adds_new_book(self):
        posting_object = {"q": "x"}
        expected_response = {
            "items": [
                {
                    "volumeInfo": {
                        "title": "book0",
                        "authors": ["John", "F"],
                        "publishedDate": "1999-01-01",
                    }
                },
                {
                    "volumeInfo": {
                        "title": "book1",
                        "authors": ["Kennedy"],
                        "publishedDate": "2000-01-01",
                    }
                },
            ]
        }
        with patch(
            "app.views_utils.requests.get", Mock(return_value=GoogleBookResponse(expected_response))
        ):
            self.client.post(self.add_url, posting_object)

        books = Book.objects.filter(Q(title="book0") | Q(title="book1"))
        for book in books:
            assert book.title in ["book0", "book1"]

    def test_book_add_POST_adds_new_book_empty_list(self):
        posting_object = {"q": "x"}

        expected_response = {"items": None}
        with patch(
            "app.views_utils.requests.get", Mock(return_value=GoogleBookResponse(expected_response))
        ):
            response = self.client.post(self.add_url, posting_object)

        self.assertEquals(response["status"], "books not added")
