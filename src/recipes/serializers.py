from rest_framework import serializers
from . import models
import accounts.models as accounts_models


class CuisineCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CuisineCountry
        fields = '__all__'


class CuisineSerializer(serializers.ModelSerializer):
    country = CuisineCountrySerializer()
    class Meta:
        model = models.Cuisine
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    cuisine = CuisineSerializer()
    class Meta:
        model = models.Ingredient
        exclude = ['recipe']


class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Direction
        exclude = ['recipe']



class DiscussionUserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = accounts_models.User
        fields = ['id', 'first_name', 'last_name', 'image']
    
    def get_image(self, obj):
        request = self.context.get('request', None)
        return obj.get_image(request)


class DiscussionSerializer(serializers.ModelSerializer):
    user_info = DiscussionUserSerializer(read_only=True, source='user')
    likes_count = serializers.SerializerMethodField()
    replies_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    class Meta:
        model = models.Discussion
        fields = "__all__"
        extra_kwargs = {
            'user': {'write_only': True},
            'likes': {'read_only': True},
        }
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_replies_count(self, obj):
        return obj.replies.count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request', None)
        if request is None:
            print('No request')
            return False
        return obj.is_liked(request.user)



class DiscussionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Discussion
        fields = "__all__"



class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Gallery
        exclude = ['recipe']


class RecipeSerializer(serializers.ModelSerializer):
    chef_user = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    ingredients = IngredientSerializer(many=True)
    directions = DirectionSerializer(many=True)
    discussions = DiscussionSerializer(many=True)
    galleries = GallerySerializer(many=True)
    
    
    class Meta:
        model = models.Recipe
        fields = '__all__'
    
    def get_chef_user(self, obj):
        return obj.chef_user.user.id

    def get_likes_count(self, obj):
        return obj.likes_count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request', None)
        if request is None:
            return False
        return obj.is_liked(request.user)