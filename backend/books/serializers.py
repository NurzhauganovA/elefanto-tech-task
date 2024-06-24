from rest_framework import serializers

from books.models import Genre, Book, Review


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class BookSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()

    def get_is_favorite(self, obj):
        return obj.favorites.filter(id=self.context['request'].user.id).exists()

    class Meta:
        model = Book
        fields = ['id', 'title', 'genre', 'author', 'publication_date', 'description', 'cover_image', 'is_favorite']
        extra_kwargs = {
            'author': {'read_only': True},
            'genre': {'read_only': True}
        }


class BookCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'genre', 'author', 'publication_date', 'description', 'cover_image']
        extra_kwargs = {
            'author': {'read_only': True},
        }


class BookAddToFavoriteSerializer(serializers.Serializer):
    class Meta:
        fields = []


class BookRemoveFromFavoriteSerializer(serializers.Serializer):
    class Meta:
        fields = []


class BookReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['author', 'text', 'rating']
        extra_kwargs = {
            'author': {'read_only': True},
        }


class BookDetailSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    def get_reviews(self, obj):
        return BookReviewsSerializer(obj.reviews.all(), many=True).data

    def get_is_favorite(self, obj):
        return obj.favorites.filter(id=self.context['request'].user.id).exists()

    def get_average_rating(self, obj):
        return obj.average_rating()

    class Meta:
        model = Book
        fields = ['id', 'title', 'genre', 'author', 'publication_date', 'description', 'cover_image', 'reviews',
                  'average_rating', 'is_favorite']


class CreateBookReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'author', 'book', 'text', 'rating')
        extra_kwargs = {
            'author': {'read_only': True},
            'book': {'read_only': True}
        }

    def validate(self, attrs):
        if attrs['rating'] not in range(1, 6):
            raise serializers.ValidationError('Rating must be in range 1-5')
        return attrs


class MyBookReviewSerializer(serializers.ModelSerializer):
    book = BookDetailSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'book', 'text', 'rating']
