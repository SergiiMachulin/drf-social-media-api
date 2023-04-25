from rest_framework import serializers
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    user_liked = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = "__all__"

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_user_liked(self, obj):
        if "request" in self.context:
            user = self.context["request"].user
            if user.is_authenticated:
                return obj.likes.filter(id=user.id).exists()
        return False


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ("user",)
