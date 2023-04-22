from rest_framework import serializers
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "user",
            "first_name",
            "last_name",
            "profile_picture",
            "bio",
            "location",
            "birthdate",
        ]
        read_only_fields = ["id", "user"]
