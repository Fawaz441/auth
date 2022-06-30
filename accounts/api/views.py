from accounts.models import User
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from utils.response import ERROR, SUCCESSFUL, CustomResponse

from .serializers import (LoginSerializer, RegisterSerializer,
                          ResetPasswordSerializer, UserSerializer)


class RegisterAPIView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        data = RegisterSerializer(data=request.data)
        if data.is_valid():
            validated_data = data.validated_data
            password_weaknesses = data.get_password_errors()
            if password_weaknesses:
                return CustomResponse(400, ERROR, password_weaknesses)
            user = User.objects.create(
                first_name=validated_data.get('first_name'),
                email=validated_data.get('email'),
                last_name=validated_data.get('last_name'),
            )
            user.set_password(validated_data.get('password'))
            user.save()
            return CustomResponse(
                201,
                SUCCESSFUL,
                message="User created succesfully"
            )
        return CustomResponse(400, ERROR, data.errors)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        data = LoginSerializer(data=request.data)
        if data.is_valid():
            validated_data = data.validated_data
            email = validated_data.get("email")
            password = validated_data.get("password")
            user = User.objects.filter(email__iexact=email).first()
            if user:
                if user.check_password(password):
                    return CustomResponse(200, SUCCESSFUL,
                                          message="Login Successful", data=UserSerializer(user).data)
                return CustomResponse(400, ERROR, "Invalid credentials")
            return CustomResponse(400, ERROR, "Invalid credentials")
        return CustomResponse(400, ERROR, data.errors)


class PasswordResetAPIView(APIView):
    """Pass in token in header => Authorization : Token {token}"""
    def post(self, request):
        data = ResetPasswordSerializer(data=request.data, context={'user':request.user})
        if data.is_valid():
            validated_data = data.validated_data
            current_password = validated_data.get("current_password")
            user = request.user
            new_password = validated_data.get("new_password")
            if request.user.check_password(new_password):
                return CustomResponse(400, ERROR, "New password cannot be the same as current password")
            if not request.user.check_password(current_password):
                return CustomResponse(400, ERROR, "Invalid current password")
            password_weaknesses = data.get_password_errors()
            if password_weaknesses:
                return CustomResponse(400, ERROR, password_weaknesses)
            user.set_password(new_password)
            user.save()
            return CustomResponse(200, SUCCESSFUL, "Password reset successfully")
        else:
            return CustomResponse(400, ERROR, data.errors)

            