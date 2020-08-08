from django.urls import reverse, resolve
from django.test import SimpleTestCase
from app.views import book_create_view


class TestUrls(SimpleTestCase):
    def setUp(self):
        self.add_url = reverse("book-add")

    def test_add_url_resolves(self):
        self.assertEquals(resolve(self.add_url).func, book_create_view)
