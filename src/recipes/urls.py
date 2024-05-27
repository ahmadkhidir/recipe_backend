from django.urls import path
from . import views


urlpatterns = [
    path("", views.RecipeListAPIView.as_view(), name="recipes"),
    path("cuisines/", views.CuisineListAPIView.as_view(), name="cuisines"),
    path("cuisines/countries/", views.CuisineCountryListAPIView.as_view(), name="cuisines_countries"),
]
