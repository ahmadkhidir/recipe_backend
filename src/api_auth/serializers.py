from rest_framework import serializers

class BasicAuthChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()


class BasicAuthResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class BasicAuthResetVerifyPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField()
    otp = serializers.IntegerField()


class GoogleAuthSerializer(serializers.Serializer):
    token = serializers.CharField()