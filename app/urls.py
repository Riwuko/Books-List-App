from django.urls import path, include
from app.views import BookViewSet, book_create_view
from rest_framework import routers

router = routers.DefaultRouter()
router.register("books", BookViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("db", book_create_view, name="db"),
]
