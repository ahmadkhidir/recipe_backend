from django.urls import path
from . import views

urlpatterns = [
    path("", views.AccountAPIView.as_view(), name="info"),
    path("register/", views.RegisterAPIView.as_view(), name="register"),
    path("register/profile/", views.ProfileAPIView.as_view(), name="register_profile"),
    path("register/chef-profile/", views.ChefProfileAPIView.as_view(), name="register_chef_profile"),
    path("public/", views.PublicAccountListAPIView.as_view(), name="public_accounts"),
    path("public/<pk>/", views.PublicAccountRetrieveAPIView.as_view(), name="public_account"),
]
