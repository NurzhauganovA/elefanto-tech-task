from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status, generics, views
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from .filters import BookFilter
from .models import Book, Genre, Review
from .permissions import IsAuthorOrSuperuser

from .serializers import GenreSerializer, BookSerializer, BookCreateUpdateSerializer, \
    CreateBookReviewSerializer, MyBookReviewSerializer, BookDetailSerializer, BookAddToFavoriteSerializer, \
    BookRemoveFromFavoriteSerializer
from .services import get_user_reviews, create_book_review, remove_book_from_favorites, add_book_to_favorites


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().select_related('author', 'genre').prefetch_related('favorites', 'reviews')
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrSuperuser]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = BookFilter
    ordering_fields = ['title', 'publication_date']
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BookCreateUpdateSerializer
        if self.action == 'retrieve':
            return BookDetailSerializer
        return BookSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = Book.objects.get(id=kwargs['pk'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class BookAddToFavoriteView(generics.GenericAPIView):
    queryset = Book.objects.all().select_related('author', 'genre').prefetch_related('favorites', 'reviews')
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookAddToFavoriteSerializer

    def post(self, request, *args, **kwargs):
        add_book_to_favorites(kwargs['pk'], request.user)
        return Response({'message': 'Book added to favorites'}, status=status.HTTP_200_OK)


class BookRemoveFromFavoriteView(generics.GenericAPIView):
    queryset = Book.objects.all().select_related('author', 'genre').prefetch_related('favorites', 'reviews')
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookRemoveFromFavoriteSerializer

    def post(self, request, *args, **kwargs):
        remove_book_from_favorites(kwargs['pk'], request.user)
        return Response({'message': 'Book removed from favorites'}, status=status.HTTP_200_OK)


class CreateBookReviewView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = CreateBookReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        create_book_review(self.kwargs['pk'], self.request.user, serializer.validated_data['text'], serializer.validated_data['rating'])

    @action(detail=True, methods=['post'])
    def create_review(self, request, *args, **kwargs):
        request.data['author'] = request.user.id
        return super().create(request, *args, **kwargs)


class MyBookReviewView(generics.ListAPIView):
    serializer_class = MyBookReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return get_user_reviews(self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class MyFavoriteBooksView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.favorite_books.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
