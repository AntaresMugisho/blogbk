from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.utils.translation import gettext_lazy as _

from .serializers import (
    UserRegistrationSerializer, 
    UserSerializer,
    PasswordUpdateSerializer
)
from .models import BlacklistedToken

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer
    

class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            
            if not refresh_token:
                return Response(
                    {"detail": "Refresh token is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"detail": "Successfully logged out"},
                status=status.HTTP_200_OK
            )
        except TokenError:
            return Response(
                {"detail": "Invalid token"},
                status=status.HTTP_400_BAD_REQUEST
            )

class PasswordUpdateView(generics.UpdateAPIView):
    serializer_class = PasswordUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_authenticated = True
        serializer.is_valid(raise_exception=True)
        
        user = self.get_object()
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({"detail": _("Password updated successfully.")}, status=status.HTTP_200_OK)

class RevokeTokenView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            
            if not refresh_token:
                return Response(
                    {"detail": "Refresh token is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"detail": "Token successfully revoked"},
                status=status.HTTP_200_OK
            )
        except TokenError:
            return Response(
                {"detail": "Invalid token"},
                status=status.HTTP_400_BAD_REQUEST
            )