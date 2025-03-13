from rest_framework import generics
from django.db.models import Avg, Count
from .models import Director, Movie, Review
from .serializers import (
    DirectorSerializer,
    MovieReviewsSerializer,
    MovieSerializer,
    ReviewSerializer,
)

# Режиссеры
class DirectorList(generics.ListCreateAPIView):  # Добавлен CreateAPIView
    queryset = Director.objects.annotate(movies_count=Count('movies'))
    serializer_class = DirectorSerializer

class DirectorDetail(generics.RetrieveUpdateDestroyAPIView):  # Добавлены Update и Destroy
    queryset = Director.objects.annotate(movies_count=Count('movies'))
    serializer_class = DirectorSerializer

# Фильмы
class MovieList(generics.ListCreateAPIView):  # Добавлен CreateAPIView
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieDetail(generics.RetrieveUpdateDestroyAPIView):  # Добавлены Update и Destroy
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

# Отзывы
class ReviewList(generics.ListCreateAPIView):  # Добавлен CreateAPIView
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):  # Добавлены Update и Destroy
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

# Фильмы с отзывами и рейтингом
class MovieReviewsList(generics.ListAPIView):
    queryset = Movie.objects.annotate(rating=Avg('reviews__stars'))
    serializer_class = MovieReviewsSerializer