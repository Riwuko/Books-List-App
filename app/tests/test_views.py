from django.test import Client,TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from app.models import Book
from app.views import BookViewSet, book_create_view

class TestViews(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = Client()
        self.add_url = reverse('book-add')
        
    def test_book_list_GET(self):
        request = self.factory.get("")
        book_list = BookViewSet.as_view({'get': 'list'})
        response = book_list(request)
        
        self.assertEquals(response.status_code,200)
    
    def test_book_detail_GET(self):
        request = self.factory.get("")
        book_detail = BookViewSet.as_view({'get': 'retrieve'})
        book = Book.objects.create(title='book',authors=['author'],published_date='1999-01-01')
        response = book_detail(request,pk=book.pk)
        
        self.assertEquals(response.status_code,200)

    def test_book_add_POST_adds_new_book(self):
        object = {
            'q':'Hobbit czyli Tam i z powrotem'
        }
        response = self.client.post(self.add_url, object)
        
        self.assertEquals(response['status'],"books added")

    def test_book_add_POST_adds_new_book_long_name(self):
        object = {
            'q':'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        }
        response = self.client.post(self.add_url, object)
        self.assertEquals(response['status'],"books not added")

  