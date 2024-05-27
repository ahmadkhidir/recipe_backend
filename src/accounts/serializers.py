from rest_framework import serializers
from phonenumbers import format_number, PhoneNumberFormat
from .models import User, Profile, ChefProfile


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email',
                  'username', 'phone_number', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['user']
        depth = 2

    def create(self, validated_data):
        instance: Profile = super().create(validated_data)
        User.objects.filter(id=instance.user.id).update(
            account_type=instance.TYPE)
        return instance


class ChefProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChefProfile
        exclude = ['user']

    def create(self, validated_data):
        instance: ChefProfile = super().create(validated_data)
        User.objects.filter(id=instance.user.id).update(
            account_type=instance.TYPE)
        return instance


class FollowSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'account_type', 'image']

    # def get_image(self, obj):
    #     try:
    #         request = self.context.get('request', None)
    #         url = obj.profile.image.url if obj.account_type == Profile.TYPE else None
    #         if request is not None and url is not None:
    #             return request.build_absolute_uri(url)
    #         return url
    #     except Exception as e:
    #         print('Error getting image', e)
    #         return None
    def get_image(self, obj):
        request = self.context.get('request', None)
        return obj.get_image(request)


class AccountSerializer(serializers.ModelSerializer):
    phone_number = serializers.SerializerMethodField()
    profile = ProfileSerializer()
    chef_profile = ChefProfileSerializer(source='chefprofile')
    followers = FollowSerializer(many=True)
    following = FollowSerializer(many=True)
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ['password']

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_phone_number(self, obj):
        return format_number(obj.phone_number, PhoneNumberFormat.INTERNATIONAL) if obj.phone_number else None


class PublicAccountSerializer(serializers.ModelSerializer):
    phone_number = serializers.SerializerMethodField()
    profile = ProfileSerializer()
    chef_profile = ChefProfileSerializer(source='chefprofile')
    followers = FollowSerializer(many=True)
    following = FollowSerializer(many=True)
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email',
                  'username', 'phone_number', 'account_type',
                  'profile', 'chef_profile', 'followers', 'following',
                  'followers_count', 'following_count']

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_phone_number(self, obj):
        return format_number(obj.phone_number, PhoneNumberFormat.INTERNATIONAL) if obj.phone_number else None
