from django.db import models
from django.core.validators import FileExtensionValidator

from utils.helpers import INGREDIENT_MEASURES


class CuisineCountry(models.Model):
    name = models.CharField(max_length=255)
    flag = models.ImageField(upload_to='flags/', null=True, blank=True)
    code = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        return self.name


class Cuisine(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='cuisines/', null=True, blank=True)
    country = models.ForeignKey(CuisineCountry, on_delete=models.CASCADE, related_name='cuisines')

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    video = models.FileField(upload_to='recipes/', validators=[FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mkv'])])
    # duration = models.DurationField()
    chef_user = models.ForeignKey("accounts.ChefProfile", on_delete=models.CASCADE, related_name='recipes')
    likes = models.ManyToManyField("accounts.User", blank=True, related_name='liked_recipes')

    def __str__(self):
        return self.name
    
    def likes_count(self):
        return self.likes.count()
    
    def is_liked(self, user):
        return self.likes.filter(id=user.id).exists()


class Ingredient(models.Model):
    cuisine = models.OneToOneField(Cuisine, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    measurement = models.CharField(max_length=20, choices=INGREDIENT_MEASURES)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')

    def __str__(self):
        return f"{self.cuisine.name}: {self.quantity} {self.measurement} on {self.recipe.name}"


class Direction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='directions')
    begin = models.TimeField()
    end = models.TimeField()
    description = models.TextField()

    def __str__(self):
        return f"{self.description}: {self.begin} - {self.end} on {self.recipe.name}"


class CookBook(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    recipes = models.ManyToManyField(Recipe, related_name='cookbooks')
    regular_user = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE, related_name='cookbooks')

    def __str__(self):
        return self.title


class Discussion(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name='discussions')
    chat = models.TextField()
    replied_to = models.ForeignKey("Discussion", on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    likes = models.ManyToManyField("accounts.User", blank=True, related_name='liked_discussions')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='discussions')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on {self.recipe.name}"
    
    def likes_count(self):
        return self.likes.count()
    
    def replies_count(self):
        return self.replies.count()
    
    def is_liked(self, user):
        return self.likes.filter(id=user.id).exists()


class Gallery(models.Model):
    image = models.ImageField(upload_to='galleries/')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='galleries')

    def __str__(self):
        return f"{self.recipe.name} gallery"