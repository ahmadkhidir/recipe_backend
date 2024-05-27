from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

from utils.helpers import ACCOUNT_TYPES
from utils.models import UUIDMixin


class User(AbstractUser, UUIDMixin):
    phone_number = PhoneNumberField(_("Phone Number"), unique=True)
    account_type = models.CharField(_("Account Type"), max_length=255, default="regular", choices=ACCOUNT_TYPES)
    following = models.ManyToManyField("User", related_name="followers", blank=True)

    def get_image(self, request):
        try:
            url = self.profile.image.url if self.account_type == Profile.TYPE else None
            if request is not None and url is not None:
                return request.build_absolute_uri(url)
            return url
        except Exception as e:
            # print('Error getting image', e)
            return None


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(_("Image"), upload_to="profiles/", blank=True, null=True)
    cover_image = models.ImageField(_("Cover Image"), upload_to="profiles/", blank=True, null=True)
    interests = models.ManyToManyField("recipes.Cuisine", related_name="interested_users", blank=True)
    dislikes = models.ManyToManyField("recipes.Cuisine", related_name="disliked_users", blank=True)

    TYPE = 'regular'
    def __str__(self):
        return self.user.username


class ChefProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(_("Bio"), blank=True, null=True)

    TYPE = 'chef'
    def __str__(self):
        return self.user.username