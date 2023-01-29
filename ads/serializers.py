
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from ads import models
from ads.models import Ad, Category, Selection
from users.models import User, UserRoles
from users.serializers import UserSerializer, UserLocationSerializer


class CategorySerializer(ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class AdListSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field="name", queryset=Category.objects.all())
    author = UserLocationSerializer()

    class Meta:
        model = Ad
        fields = ['name', 'author', 'price', 'category']


class AdDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    category = serializers.SlugRelatedField(slug_field="name", queryset=Category.objects.all())

    class Meta:
        model = Ad
        fields = '__all__'


class SelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = '__all__'


class SelectionCreateSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all(), required=False)

    def create(self, validated_data):
        request = self.context.get("request")

        if "author" not in validated_data:
            validated_data["author"] = request.user
        elif "author" in validated_data and request.user.role == UserRoles.MEMBER \
                and request.user != validated_data["author"]:
            raise ValidationError("Нет доступа ")
        return super().create(validated_data)

    class Meta:
        model = Selection
        fields = '__all__'
