from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, logout
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({
            'user_id': self.user.id,
            'email': self.user.email,
            'username': self.user.username,
        })
        return data

class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user

        # Log in the user with Django session
        login(request, user)

        # Return JWT tokens + username
        data = response.data
        data["username"] = user.username
        return Response(data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, req):
        try:
            refresh_token = req.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            logout(req)
            return Response({"detail": "Logout successful"}, status=200)  
        except Exception as e:
            return Response({"detail": "Invalid token"}, status=400)