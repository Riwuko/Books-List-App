from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Book
from .serializers import BookSerializer

@api_view(['GET'])
def bookListView(request):
    books = Book.objects.all()
    serializer = BookSerializer(books,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def bookDetailView(request,id):
    books = Book.objects.get(id=id)
    serializer = BookSerializer(books,many=False)
    return Response(serializer.data)


@api_view(['POST'])
def bookCreateView(request,id):
    serializer = BookSerializer(request.data)

    if serializer.is_valid():
        serializer.save()
        
    return Response(serializer.data)