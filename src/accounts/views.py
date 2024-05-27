from rest_framework import generics
from rest_framework import permissions
from django_filters import rest_framework as django_filters
from . import serializers


class RegisterAPIView(generics.CreateAPIView):
    """
    Register a new user.
    """
    serializer_class = serializers.RegisterSerializer
    permission_classes = [permissions.AllowAny]
    queryset = serializers.User.objects.all()


class ProfileAPIView(generics.CreateAPIView):
    """
    Create user profile.
    """
    serializer_class = serializers.ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = serializers.Profile.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ChefProfileAPIView(generics.CreateAPIView):
    """
    Create user profile.
    """
    serializer_class = serializers.ChefProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = serializers.ChefProfile.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AccountAPIView(generics.RetrieveAPIView):
    """
    Retrive user information.
    """
    serializer_class = serializers.AccountSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = serializers.User.objects.all()

    def get_object(self):
        return self.request.user


class PublicAccountListAPIView(generics.ListAPIView):
    """
    List all public accounts.
    """
    serializer_class = serializers.PublicAccountSerializer
    permission_classes = [permissions.AllowAny]
    queryset = serializers.User.objects.all()
    filter_backends = [django_filters.DjangoFilterBackend]
    filterset_fields = ['account_type']


class PublicAccountRetrieveAPIView(generics.RetrieveAPIView):
    """
    Retrieve public account information.
    """
    serializer_class = serializers.PublicAccountSerializer
    permission_classes = [permissions.AllowAny]
    queryset = serializers.User.objects.all()
    filter_backends = [django_filters.DjangoFilterBackend]
    filterset_fields = ['account_type']