from typing import Any
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
import string
from django.utils.crypto import get_random_string

UserModel = get_user_model()


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        email = username
        if email is None:
            email = kwargs.get(UserModel.EMAIL_FIELD)
        if email is None or password is None:
            return
        try:
            user = UserModel.objects.get(email=email)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except UserModel.DoesNotExist:
            return None


class GoogleBackend(ModelBackend):
    def authenticate(self, request: HttpRequest, token, **kwargs) -> AbstractBaseUser | None:
        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.GOOGLE_CLIENT_ID)

            # Or, if multiple clients access the backend server:
            # idinfo = id_token.verify_oauth2_token(token, requests.Request())
            # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
            #     raise ValueError('Could not verify audience.')

            # If the request specified a Google Workspace domain
            # if idinfo['hd'] != DOMAIN_NAME:
            #     raise ValueError('Wrong domain name.')

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            userid = idinfo['sub']
            email = idinfo['email']
            first_name = idinfo['given_name']
            last_name = idinfo['family_name']

            user = UserModel.objects.filter(email=email)
            if user.exists():
                return user.first
            else:
                user = UserModel.objects.create(
                    email=email,
                    username=email,
                    first_name=first_name,
                    last_name=last_name,)
                random_password = get_random_string(10, string.ascii_letters+string.digits)
                user.set_password(random_password)
                user.save()
                return user


        except ValueError:
            # Invalid token
            return
