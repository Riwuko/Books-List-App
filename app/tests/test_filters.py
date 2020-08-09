from django.test import Client, TestCase
from django.urls import reverse

from app.models import Book
from app.views_api import BookFilter


class TestModels(TestCase):
    def setUp(self):
        self.client = Client()
        self.list_url = reverse("book-list")
        self.id_1 = 1
        self.id_2 = 2
        self.id_3 = 3

        Book.objects.create(
            pk=self.id_1, title="book0", authors=["John"], published_date="1999-01-01"
        )
        Book.objects.create(
            pk=self.id_2, title="book1", authors=["Fitzgerald"], published_date="2000-01-01"
        )
        Book.objects.create(
            pk=self.id_3, title="book2", authors=["Kennedy"], published_date="2000-01-02"
        )

    def test_filter_title(self):
        response = self.client.get(self.list_url + "?title=book0")
        expected_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.id_1,
                    "title": "book0",
                    "authors": ["John"],
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

    def test_filter_title_empty_result(self):
        response = self.client.get(self.list_url + "?title=book3")
        expected_response = {"count": 0, "next": None, "previous": None, "results": []}
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding="utf8"), expected_response)

    def test_ordering_ascending(self):
        response = self.client.get(self.list_url + "?ordering=published_date")
        expected_response = {
            "count": 3,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "title": "book0",
                    "authors": ["John"],
                    "published_date": "1999-01-01",
                    "categories": None,
                    "average_rating": None,
                    "rating_count": None,
                    "thumbnail": None,
                },
                {
                    "id": 2,
                    "title": "book1",
                    "authors": ["Fitzgerald"],
                    "published_date": "2000-01-01",
                    "categories": None,
                    "average_rating": None,
                    "rating_count": None,
                    "thumbnail": None,
                },
                {
                    "id": 3,
                    "title": "book2",
                    "authors": ["Kennedy"],
                    "published_date": "2000-01-02",
                    "categories": None,
                    "average_rating": None,
                    "rating_count": None,
                    "thumbnail": None,
                },
            ],
        }
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding="utf8"), expected_response)

    def test_ordering_descending(self):
        response = self.client.get(self.list_url + "?ordering=-published_date")
        expected_response = {
            "count": 3,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 3,
                    "title": "book2",
                    "authors": ["Kennedy"],
                    "published_date": "2000-01-02",
                    "categories": None,
                    "average_rating": None,
                    "rating_count": None,
                    "thumbnail": None,
                },
                {
                    "id": 2,
                    "title": "book1",
                    "authors": ["Fitzgerald"],
                    "published_date": "2000-01-01",
                    "categories": None,
                    "average_rating": None,
                    "rating_count": None,
                    "thumbnail": None,
                },
                {
                    "id": 1,
                    "title": "book0",
                    "authors": ["John"],
                    "published_date": "1999-01-01",
                    "categories": None,
                    "average_rating": None,
                    "rating_count": None,
                    "thumbnail": None,
                },
            ],
        }
        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding="utf8"), expected_response)
