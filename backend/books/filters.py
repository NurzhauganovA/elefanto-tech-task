import django_filters
from .models import Book


class BookFilter(django_filters.FilterSet):
    publication_date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Book
        fields = ['genre', 'author', 'publication_date']
