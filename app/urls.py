from django.urls import path,include
from . import views
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register('book-list', views.BookViewSet)

# urlpatterns = [
#     path('',include(router.urls))
# ]

urlpatterns = [
    path('',views.bookListView, name='book-list'),
    path('book-detail/<int:id>', views.bookDetailView, name='book-detail'),
    path('book-create',views.bookCreateView,name='book-create'),
]