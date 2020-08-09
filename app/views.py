from django.views.decorators.csrf import csrf_exempt
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter


from app.views_api import BookFilter
from app.views_utils import download_items, find_books_for_update, prepare_items
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
@csrf_exempt
def book_create_view(request):
    print(f'\n\n{request.data}\n\n')
    serializer = QuerySerializer(data=request.data)
    response = Response()
    if (serializer.is_valid() or True):
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
