from typing import Any, Tuple

from django.contrib.auth import get_user_model
from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework.generics import get_object_or_404
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from user.serializers import UserSerializer
from .models import Follower
from .serializers import FollowerSerializer


class FollowMixin:
    @staticmethod
    def get_following_and_followers(user) -> Tuple[ReturnDict, ReturnDict]:
        following = (
            Follower.objects.filter(user=user)
            .select_related("followee")
            .values_list("followee", flat=True)
        )
        followers = (
            Follower.objects.filter(followee=user)
            .select_related("user")
            .values_list("user", flat=True)
        )
        following_users = get_user_model().objects.filter(pk__in=following)
        follower_users = get_user_model().objects.filter(pk__in=followers)
        following_serializer = UserSerializer(following_users, many=True)
        follower_serializer = UserSerializer(follower_users, many=True)
        return following_serializer.data, follower_serializer.data


class FollowView(FollowMixin, APIView):
    serializer_class = FollowerSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        description="Follow a user by ID.",
        request=FollowerSerializer,
        responses={201: FollowerSerializer},
    )
    def post(self, request, pk: int, *args, **kwargs) -> Response:
        followee = get_user_model().objects.filter(pk=pk).first()
        if not followee:
            return Response(
                {"detail": "The user with the specified ID does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = request.user
        if user.id == followee.id:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            Follower.objects.create(user=user, followee=followee)
            following, followers = self.get_following_and_followers(user)
            return Response(
                {
                    "detail": "Successfully followed.",
                    "following": following,
                    "followers": followers,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception:
            return Response(
                {"detail": "Failed to follow."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UnfollowView(FollowMixin, generics.DestroyAPIView):
    serializer_class = FollowerSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Follower.objects.all()

    def get_object(self) -> Any:
        user = self.request.user
        followee_pk = self.kwargs.get("pk")
        return get_object_or_404(self.queryset, user=user, followee_id=followee_pk)

    @extend_schema(
        description="Unfollow a user by ID.",
        request=FollowerSerializer,
        responses={204: None},
    )
    def delete(self, request, *args, **kwargs) -> Response:
        try:
            instance = self.get_object()
        except Http404:
            return Response(
                {"detail": "You are not following this user."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        followee = instance.followee

        if request.user == followee:
            return Response(
                {"detail": "You cannot unfollow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        self.perform_destroy(instance)
        following, followers = self.get_following_and_followers(request.user)
        return Response(
            {
                "detail": "Successfully unfollowed.",
                "following": following,
                "followers": followers,
            },
            status=status.HTTP_200_OK,
        )
