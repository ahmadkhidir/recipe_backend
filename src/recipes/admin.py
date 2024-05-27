from django.contrib import admin
from . import models


admin.site.register([
    models.Cuisine,
    models.CuisineCountry,
    models.Recipe,
    models.Ingredient,
    models.Direction,
    models.Gallery,
    models.Discussion,
    models.CookBook,
    ])