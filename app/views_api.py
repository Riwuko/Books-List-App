from django_filters import rest_framework as filters


from app.models import Book


class BookFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr="icontains")
    author = filters.CharFilter(lookup_expr="icontains")
    categories = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Book
        fields = ("title", "author", "categories")
