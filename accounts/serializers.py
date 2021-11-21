from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django import forms
from rest_framework.serializers import CharField
from django.db.models import Q
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserCreateSerializer(ModelSerializer):

    password2 = serializers.CharField(label="Confirm password")
    token = CharField(allow_blank=True, read_only=True)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "password",
            "password2",
            "email",
            "token",
        )

        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True},
        }

    def create(self, validated_data):

        first_name = validated_data["first_name"]
        last_name = validated_data["last_name"]
        email = validated_data["email"]
        password = validated_data["password"]
        username = validated_data["username"]

        user_obj = User(
            first_name=first_name, last_name=last_name, username=username, email=email
        )
        user_obj.set_password(password)
        user_obj.save()
        token = Token.objects.create(user=user_obj)
        validated_data["token"] = token
        return validated_data

    def validate_password(self, value):
        data = self.get_initial()
        password1 = data.get("password2")
        if password1 != value:
            raise ValueError("passwords must be equal")
        return value

    def validate(self, data):

        email = data["email"]
        user = User.objects.filter(email=email)
        if user:
            raise forms.ValidationError("user with this email already exists")
        return data


class UserLoginSerializer(ModelSerializer):

    token = CharField(allow_blank=True, read_only=True)
    username = CharField(allow_blank=True, required=False)
    email = CharField(label="User email")

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "email",
            "token",
        )

        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):

        user_obj = 0
        username = data.get("username")
        password = data.get("password")
        email = data.get("username")

        if not (username and password):
            raise forms.ValidationError("username and email are requireded")

        user = User.objects.filter(Q(username=username) | Q(email=email))

        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise forms.ValidationError("This username/email is not valid")

        if not user_obj.check_password(password):
            raise forms.ValidationError("Password id incorrect")

        token = Token.objects.get(user=user_obj)
        data["token"] = token

        return data


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")
