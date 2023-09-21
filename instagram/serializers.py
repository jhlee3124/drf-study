from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Post


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["username", "email"]


# 추가 field 직접 지정하는 스타일
class PostSerializer(ModelSerializer):
    username = serializers.ReadOnlyField(source="author.username")
    email = serializers.ReadOnlyField(source="author.email")

    class Meta:
        model = Post
        fields = [
            "pk",
            "username",
            "email",
            "ip",
            "is_public",
            "message",
            "created_at",
            "updated_at",
        ]


# # nested serializer 이용하는 스타일
# class PostSerializer(ModelSerializer):
#     author = AuthorSerializer()

#     class Meta:
#         model = Post
#         fields = [
#             "pk",
#             "author",
#             "message",
#             "is_public",
#             "created_at",
#             "updated_at",
#         ]
