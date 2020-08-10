from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from rest_framework import request

from app.views_api import BookFilter
from app.views_utils import download_items, find_books_for_update, prepare_items, try_and_get_json
from .models import Book
from .serializers import BookSerializer, QuerySerializer


class BookViewSet(ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = PageNumberPagination

    ordering_fields = ("published_date",)
    ordering = ("pk",)
    filterset_class = BookFilter


@api_view(["POST"])
def book_create_view(request):
    response = Response()
    request_data = request.data
    request_data_is_json = try_and_get_json(str(request_data))

    if not request_data_is_json:
        response["status"] = "Wrong books request"
        return response

    if not request_data.get("q"):
        request_data = request_data.get("_content")
        request_data_json = try_and_get_json(str(request_data))
        print(f'\n\n{request_data_json}\n\n')
        request_data = eval(request_data_json[0])

    serializer = QuerySerializer(data=request_data)

    if serializer.is_valid():
        q = serializer.data["q"]

        items = download_items(q)

        if items is not None:
            books = prepare_items(items)
            books_for_update = find_books_for_update(books)

            Book.objects.bulk_update(
                [book for book in books_for_update],
                fields=(
                    "title",
                    "author",
                    "published_date",
                    "categories",
                    "average_rating",
                    "rating_count",
                    "thumbnail",
                ),
            )

            Book.objects.bulk_create([Book(**book) for book in books], ignore_conflicts=True)

            response["status"] = "books added"
            return response

    response["status"] = "books not added"
    return response
