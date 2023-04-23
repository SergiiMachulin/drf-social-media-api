from rest_framework import serializers
from .models import Follower


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ("user", "followee", "followed_at")
