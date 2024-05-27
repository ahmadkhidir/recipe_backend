import django_filters.rest_framework as filters
from . import models


class CuisineFilter(filters.FilterSet):
    class Meta:
        model = models.Cuisine
        fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains'],
            'country__name': ['exact', 'icontains'],
            'country__id': ['exact'],
            'country__code': ['exact', 'icontains'],
        }


class CuisineCountryFilter(filters.FilterSet):
    class Meta:
        model = models.CuisineCountry
        fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains'],
            'code': ['exact', 'icontains'],
        }