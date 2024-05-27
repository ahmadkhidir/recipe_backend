from rest_framework_simplejwt import views as jwt
from rest_framework import views, permissions, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from . import serializers
from accounts.models import User
from utils.helpers import Email, OTP
from django.shortcuts import render
from django.conf import settings

class BasicAuthView(jwt.TokenObtainPairView):
    pass

class BasicAuthRefreshView(jwt.TokenRefreshView):
    pass

class BasicAuthVerifyView(jwt.TokenVerifyView):
    pass

class BasicAuthChangePassword(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.BasicAuthChangePasswordSerializer
    

    @swagger_auto_schema(
            request_body=serializer_class,
            responses={
                status.HTTP_200_OK: serializer_class,
            }
    )
    def post(self, request: Request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            old_password= serializer.validated_data.get('old_password')
            new_password= serializer.validated_data.get('new_password')
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({
                "detail": "The old password is not correct"
            }, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BasicAuthResetPassword(views.APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.BasicAuthResetPasswordSerializer

    @swagger_auto_schema(
            request_body=serializer_class,
            responses={
                status.HTTP_200_OK: serializer_class,
            }
    )
    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({
                    "detail": "User not found"
                }, status=status.HTTP_404_NOT_FOUND)
            else:
                otp = OTP.generate_otp()
                Email.send_reset_otp(email, otp)
            return Response({
                "detail": "An OTP has been sent to your email"
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BasicAuthResetVerifyPassword(views.APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.BasicAuthResetVerifyPasswordSerializer

    @swagger_auto_schema(
            request_body=serializer_class,
            responses={
                status.HTTP_200_OK: serializer_class,
            }
    )
    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            new_password = serializer.validated_data.get('new_password')
            otp = serializer.validated_data.get('otp')
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({
                    "detail": "User not found"
                }, status=status.HTTP_404_NOT_FOUND)
            else:
                is_valid = OTP.verify_otp(otp)
                if not is_valid:
                    return Response({
                        "detail": "The OTP is not valid"
                    }, status=status.HTTP_406_NOT_ACCEPTABLE)
                user.set_password(new_password)
                user.save()
            return Response({
                "detail": "Your account password has been successfully reset. Please login to continue."
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoogleAuthView(jwt.TokenViewBase):
    serializer_class = serializers.GoogleAuthSerializer


class GoogleClientAuthView(views.View):
    def get(self, request, *args, **kwargs):
        context = {"GOOGLE_CLIENT_ID": settings.GOOGLE_CLIENT_ID}
        return render(request, "api_auth/google_oauth.html", context)