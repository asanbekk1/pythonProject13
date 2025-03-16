from rest_framework import serializers
from .models import Director, Movie, Review

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'name', 'movies_count']

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long.")
        if len(value) > 255:
            raise serializers.ValidationError("Name cannot be longer than 255 characters.")
        return value

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'duration', 'director']

    def validate_title(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("Title cannot be empty.")
        if len(value) > 255:
            raise serializers.ValidationError("Title cannot be longer than 255 characters.")
        return value

    def validate_description(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("Description cannot be empty.")
        return value

    def validate_duration(self, value):
        if value <= 0:
            raise serializers.ValidationError("Duration must be a positive number.")
        return value

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars', 'movie']

    def validate_text(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("Text cannot be empty.")
        return value

    def validate_stars(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Stars must be between 1 and 5.")
        return value

class MovieReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'title', 'reviews', 'rating']

    def get_rating(self, obj):
        return obj.reviews.aggregate(Avg('stars'))['stars__avg'] or 0