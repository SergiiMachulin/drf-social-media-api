from django.contrib.auth import get_user_model
from rest_framework import serializers

from userprofile.serializers import UserProfileSerializer


class UserSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    profile = UserProfileSerializer(source="userprofile", read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "is_staff",
            "following",
            "followers",
            "profile",
        )
        read_only_fields = ("is_staff", "following", "followers")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, set the password correctly and return it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user

    def get_following(self, obj):
        """Get a list of users the current user is following"""
        return obj.followees.all().values_list("email", flat=True)

    def get_followers(self, obj):
        """Get a list of users following the current user"""
        return obj.followers.all().values_list("email", flat=True)
