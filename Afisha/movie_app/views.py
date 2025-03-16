from rest_framework import generics
from rest_framework.exceptions import ValidationError
from django.db.models import Avg, Count
from .models import Director, Movie, Review
from .serializers import (
    DirectorSerializer,
    MovieSerializer,
    ReviewSerializer,
    MovieReviewsSerializer,
)

# Режиссеры
class DirectorList(generics.ListCreateAPIView):
    queryset = Director.objects.annotate(movies_count=Count('movies'))
    serializer_class = DirectorSerializer

class DirectorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.annotate(movies_count=Count('movies'))
    serializer_class = DirectorSerializer

# Фильмы
class MovieList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def perform_create(self, serializer):
        director_id = self.request.data.get('director')
        if not Director.objects.filter(id=director_id).exists():
            raise ValidationError("Director with this ID does not exist.")
        serializer.save()

class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

# Отзывы
class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

# Фильмы с отзывами и рейтингом
class MovieReviewsList(generics.ListAPIView):
    queryset = Movie.objects.annotate(rating=Avg('reviews__stars'))
    serializer_class = MovieReviewsSerializer