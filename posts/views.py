from django.db.models import Q, QuerySet
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from permissions.permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer


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

    def filter_by_hashtags(self, queryset):
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
