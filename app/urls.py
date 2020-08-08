from django.urls import path, include
from app.views import BookViewSet, book_create_view
from rest_framework import routers

router = routers.DefaultRouter()
router.register("book-list", BookViewSet)

urlpatterns = [path("", include(router.urls)), path("book-add", book_create_view, name="book-add")]
