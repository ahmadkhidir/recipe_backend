from django.urls import path
from . import views

urlpatterns = [
    path("basic/login/", views.BasicAuthView.as_view(), name="basic_login"),
    path("basic/login/refresh/", views.BasicAuthRefreshView.as_view(), name="basic_login_refresh"),
    path("basic/login/verify/", views.BasicAuthVerifyView.as_view(), name="basic_login_verify"),
    path("basic/password/change/", views.BasicAuthChangePassword.as_view(), name="basic_password_change"),
    path("basic/password/reset/", views.BasicAuthResetPassword.as_view(), name="basic_password_reset"),
    path("basic/password/reset/verify/", views.BasicAuthResetVerifyPassword.as_view(), name="basic_password_reset_verify"),
    path("oauth/google/", views.GoogleAuthView.as_view(), name="google_oauth"),
    path("oauth/google/client/", views.GoogleClientAuthView.as_view(), name="google_oauth_client"),
]