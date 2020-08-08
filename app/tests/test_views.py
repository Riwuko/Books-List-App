from django.db.models import Q
from django.test import Client,TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory, RequestsClient
from unittest.mock import Mock, patch

from app.models import Book
from app.views import BookViewSet, book_create_view
from app.tests.tests_utils import GoogleBookResponse

class TestViews(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = Client()
        self.add_url = reverse('book-add')
        self.list_url = reverse('book-list')

        Book.objects.create(pk=1,title='book',authors=['author'],published_date='1999-01-01')
        
    def test_book_list_GET_positive(self):
        response = self.client.get(self.list_url)
        expected_response = {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                    "id": 1,
                    "title": "book",
                    "authors": [
                        "author"
                    ],
                    "published_date": "1999-01-01",
                    "categories": None,
                    "average_rating": None,
                    "rating_count": None,
                    "thumbnail": None
                    }
        ]}


        self.assertEquals(response.status_code,200)
        self.assertJSONEqual(str(response.content,encoding='utf8'),expected_response)
    
    def test_book_list_GET_negative(self):
        response = self.client.get(self.list_url)
        
        expected_response = {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                    "id": 1,
                    "title": "book",
                    "authors": [
                        "author"
                    ],
                    "published_date": "1999-01-02",
                    "categories": None,
                    "average_rating": None,
                    "rating_count": None,
                    "thumbnail": None
                    }
        ]}


        self.assertEquals(response.status_code,200)
        self.assertJSONNotEqual(str(response.content,encoding='utf8'),expected_response)
    
    # def test_book_detail_GET(self):
    #     request = self.factory.get("")
    #     book_detail = BookViewSet.as_view({'get': 'retrieve'})
    #     response = book_detail(request,pk=book.pk)
        
        
    #     self.assertEquals(response.status_code,200)


    def test_book_add_POST_adds_new_book(self):
        object = {
            'q':'Hobbit czyli Tam i z powrotem'
        }

        expected_response = {
                'items': [
                    {
                        'volumeInfo': {
                            'authors': ['John','F'],
                            'title': 'book0',
                            'publishedDate':'1999-01-01'
                        }
                    },
                    {
                        'volumeInfo': {
                            'authors': ['Kennedy'],
                            'title': 'book1',
                            'publishedDate':'2000-01-01'
                        }
                    },
                ]
            }
        with patch('app.views_utils.requests.get',Mock(return_value=GoogleBookResponse(expected_response))):
             response = self.client.post(self.add_url, object)

        books = Book.objects.filter(Q(title='book1') | Q(title='book2'))
        for book in books:
            assert book.title in ['book0','book1']
                

def test_book_add_POST_adds_new_book_empty_list(self):
        object = {
            'q':'Hobbit czyli Tam i z powrotem'
        }

        expected_response = {
                'items': []
            }
        with patch('app.views_utils.requests.get',Mock(return_value=GoogleBookResponse(expected_response))):
             response = self.client.post(self.add_url, object)

        self.assertEquals(response['status'],"books not added")