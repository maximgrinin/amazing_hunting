from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User
from authentication.serializers import UserCreateSerializer


class UserCreateView(CreateAPIView):
    model = User
    serializer_class = UserCreateSerializer


class Logout(APIView):
    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
