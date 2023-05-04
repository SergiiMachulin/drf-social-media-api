from typing import Any

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """
    Create a new user
    """

    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update the authenticated user
    """

    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> Any:
        return self.request.user


class UserFollowersView(generics.ListAPIView):
    """
    Retrieve the list of users that the authenticated user is following
    """

    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> Any:
        return self.request.user.following.prefetch_related("following", "followers")


class UserFollowingView(generics.ListAPIView):
    """
    Retrieve the list of users that are following the authenticated user
    """

    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> Any:
        return self.request.user.followers.prefetch_related("following", "followers")
