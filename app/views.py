from django.shortcuts import render

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import Book
from .serializers import BookSerializer

from app.views_api import download_items, prepare_items


class BookViewSet(ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = PageNumberPagination

@api_view(['POST'])
def bookCreateView(request):
    items = download_items(request.data)
    prepare_items(items)
    html = "<html><body>It is now.</body></html>"
    return Response(html)

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