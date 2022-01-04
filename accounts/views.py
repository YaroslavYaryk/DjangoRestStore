from django.contrib.auth import get_user_model
from .serializers import UserCreateSerializer, UserLoginSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.authtoken.models import Token
from rest_framework import status
import jwt, datetime

User = get_user_model()
# Create your views here.


class UserCreateView(CreateAPIView):
    """User create view"""

    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserLoginView(APIView):
    """User create view"""

    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    """
    Try to login a customer (food orderer)
    """

    def post(self, request):
        data = request.data
        try:
            username = data['username']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:
            user_token = user.auth_token.key
        except:
            user_token = Token.objects.create(user=user)

        data = {'token': user_token}
        return Response(data=data, status=status.HTTP_200_OK)

