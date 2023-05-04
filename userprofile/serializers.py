from rest_framework import serializers
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "user",
            "profile_picture",
            "bio",
            "location",
            "birthdate",
        ]
        read_only_fields = ("user",)
