from django.urls import path
from rest_framework import routers

from . import views


router = routers.DefaultRouter()

router.register(r'genre', views.GenreViewSet, basename='genre')
router.register(r'', views.BookViewSet, basename='book')

urlpatterns = router.urls

urlpatterns += [
    path('<int:pk>/add-to-favorite', views.BookAddToFavoriteView.as_view()),
    path('<int:pk>/remove-from-favorite', views.BookRemoveFromFavoriteView.as_view()),

    path('<int:pk>/create-review', views.CreateBookReviewView.as_view(), name='create-review'),
    path('my-reviews', views.MyBookReviewView.as_view(), name='my-reviews'),

    path('my-favorite-books', views.MyFavoriteBooksView.as_view(), name='my-favorite-books'),
]
