from rest_framework import generics, permissions
from . import models, serializers, filters
from django_filters import rest_framework as django_filters


class CuisineListAPIView(generics.ListAPIView):
    """
    List all cuisines.
    """
    queryset = models.Cuisine.objects.all()
    serializer_class = serializers.CuisineSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [django_filters.DjangoFilterBackend]
    filterset_class = filters.CuisineFilter


class CuisineCountryListAPIView(generics.ListAPIView):
    """
    List all cuisines countries.
    """
    queryset = models.CuisineCountry.objects.all()
    serializer_class = serializers.CuisineCountrySerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [django_filters.DjangoFilterBackend]
    filterset_class = filters.CuisineCountryFilter


class RecipeListAPIView(generics.ListAPIView):
    """
    List all recipes.
    """
    queryset = models.Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [django_filters.DjangoFilterBackend]
    filterset_fields = ['name']