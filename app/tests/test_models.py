from django.test import Client,TestCase
from django.urls import reverse

from app.models import Book
from app.views import BookViewSet
from app.views_api import BookFilter

class TestModels(TestCase):

    def setUp(self):
        self.client = Client()

        Book.objects.create(pk=1,title='book0',authors=['John'],published_date='1999-01-01')
        Book.objects.create(pk=2,title='book1',authors=['Fitzgerald'],published_date='2000-01-01')
        Book.objects.create(pk=3,title='book2',authors=['Kennedy'],published_date='2000-01-02')
    
    def test_filter_title_positive(self):
        response = self.client.get(reverse('book-list')+'?title=book0')
        expected_response = {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [
            {
                "id": 1,
                "title": "book0",
                "authors": [
                    "John"
                ],
                "published_date": "1999-01-01",
                "categories": None,
                "average_rating": None,
                "rating_count": None,
                "thumbnail": None
            }
        ]
    }
        self.assertEquals(response.status_code,200)
        self.assertJSONEqual(str(response.content,encoding='utf8'),expected_response)
    
        

    def test_filter_title_negative(self):
        pass

    def test_filter_author_positive(self):
        pass

    def test_filter_author_negative(self):
        pass

    def test_ordering_positive(self):
        pass

    def test_ordering_negative(self):
        pass