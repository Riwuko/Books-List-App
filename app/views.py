from django.shortcuts import render

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter

from .models import Book
from .serializers import BookSerializer

from app.views_api import BookFilter, download_items, prepare_items

class BookViewSet(ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = PageNumberPagination

    ordering_fields = ('published_date',)
    filterset_class = BookFilter

@api_view(['POST'])
def bookCreateView(request):
    items = download_items(request.data)
    books = prepare_items(items)

    #Book.objects.bulk_create(books,ignore_conflicts=True)
    # for book in books:
    #     _,created = Book.objects.get_or_create(book)
    # print(created)

    return Response({'status':'finished'})

#     @api_view(['POST'])
# def bookCreateView(request):
#     serializer = BookPostSerializer(data=request.data)
#     print(request.data)
#     if serializer.is_valid():
#         print(serializer.data['field'])
#         download_books(serializer.data['field'])
#     else:
#         print(serializer.errors)
#     html = "<html><body>It is now.</body></html>"
#     return Response(html)