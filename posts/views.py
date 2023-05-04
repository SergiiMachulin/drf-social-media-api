from typing import Any

from django.db.models import Q, QuerySet
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from permissions.permissions import IsOwnerOrReadOnly
from .models import Post, Comment
from .serializers import PostSerializer, PostCreateSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    """Retrieve own posts and posts of users are followed by. Also, it is available to retrieve posts by hashtags"""

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="hashtags",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Filter posts by one or more hashtags. Multiple hashtags can be provided as a comma-separated list.",
                examples=[
                    OpenApiExample(
                        "Example 1",
                        summary="Filter posts by a single hashtag",
                        value="travel",
                    ),
                    OpenApiExample(
                        "Example 2",
                        summary="Filter posts by multiple hashtags",
                        value="travel,nature",
                    ),
                ],
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(description="Create a new post", tags=["posts"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(description="Retrieve a specific post by ID", tags=["posts"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(description="Update a specific post by ID", tags=["posts"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(description="Partial update a specific post by ID", tags=["posts"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(description="Delete a specific post by ID", tags=["posts"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def filter_by_hashtags(self, queryset) -> Any:
        hashtags = self.request.query_params.get("hashtags")
        if hashtags:
            hashtags = hashtags.split(",")
            for hashtag in hashtags:
                queryset = queryset.filter(hashtags__contains=f"#{hashtag}")
        return queryset

    @extend_schema(
        description="Retrieve only posts of users are followed by",
        tags=["posts"],
    )
    @action(detail=False, pagination_class=PageNumberPagination)
    def following(self, request) -> Response:
        queryset = Post.objects.select_related("user").filter(
            user__in=self.request.user.user_followees.all()
        )
        queryset = self.filter_by_hashtags(queryset)
        paginator = self.pagination_class()
        queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def get_queryset(self) -> QuerySet:
        followees = self.request.user.user_followees.all()
        queryset = Post.objects.select_related("user").filter(
            Q(user=self.request.user) | Q(user__in=followees)
        )
        queryset = self.filter_by_hashtags(queryset)
        return queryset

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return PostCreateSerializer
        return PostSerializer

    @extend_schema(
        description="Like the post by ID",
        tags=["posts"],
        request=None,
        responses={
            200: PostSerializer,
            400: "Invalid post ID or user already liked the post",
            401: "Authentication credentials were not provided",
        },
    )
    @action(
        detail=True, methods=["post"], permission_classes=[IsAuthenticated, AllowAny]
    )
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        post.likes.add(user)
        serializer = self.get_serializer(post)
        return Response(serializer.data)

    @extend_schema(
        description="Unlike the post by ID",
        tags=["posts"],
        request=None,
        responses={
            200: PostSerializer,
            400: "Invalid post ID or user has not liked the post",
            401: "Authentication credentials were not provided",
        },
    )
    @action(
        detail=True, methods=["post"], permission_classes=[IsAuthenticated, AllowAny]
    )
    def unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user
        post.likes.remove(user)
        serializer = self.get_serializer(post)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
