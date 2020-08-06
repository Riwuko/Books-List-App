from django.shortcuts import render

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import Book
from .serializers import BookSerializer


class BookViewSet(ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = PageNumberPagination

@api_view(['POST'])
def bookCreateView(request,id):
    serializer = BookSerializer(request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)