from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "content",
            "image",
            "created_at",
            "hashtags",
        ]
        read_only_fields = ("user",)
