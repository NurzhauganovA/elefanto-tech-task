from books.models import Book, Genre, Review
from rest_framework.exceptions import ValidationError


def add_book_to_favorites(book_id, user):
    book = Book.objects.get(id=book_id)
    if book.favorites.filter(id=user.id).exists():
        raise ValidationError({'message': 'Book already in favorites'})

    book.favorites.add(user)


def remove_book_from_favorites(book_id, user):
    book = Book.objects.get(id=book_id)
    if not book.favorites.filter(id=user.id).exists():
        raise ValidationError({'message': 'Book not in favorites'})

    book.favorites.remove(user)


def create_book_review(book_id, user, text, rating):
    book = Book.objects.get(id=book_id)
    if book.reviews.filter(author=user).exists():
        raise ValidationError({'message': 'You already reviewed this book'})

    review = Review.objects.create(author=user, book=book, text=text, rating=rating)
    return review


def get_user_reviews(user):
    return Review.objects.filter(author=user).select_related('book', 'book__genre').only(
        'id', 'book__title', 'book__genre__name', 'book__publication_date', 'book__description', 'text', 'rating'
    )
