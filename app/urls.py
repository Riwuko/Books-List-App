from django.urls import path,include
from app.views import BookViewSet, bookCreateView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('book-list', BookViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('book-add',bookCreateView,name='book-add')
]
