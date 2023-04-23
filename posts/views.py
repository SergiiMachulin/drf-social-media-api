from django.db.models import Q, QuerySet
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

    def filter_by_hashtags(self, queryset):
        hashtags = self.request.query_params.get("hashtags")
        if hashtags:
            hashtags = hashtags.split(",")
            for hashtag in hashtags:
                queryset = queryset.filter(hashtags__contains=f"#{hashtag}")
        return queryset

    @action(detail=False, pagination_class=PageNumberPagination)
    def following(self, request) -> Response:
        queryset = Post.objects.filter(user__in=self.request.user.user_followees.all())
        queryset = self.filter_by_hashtags(queryset)
        paginator = self.pagination_class()
        queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def get_queryset(self) -> QuerySet:
        followees = self.request.user.user_followees.all()
        queryset = Post.objects.filter(
            Q(user=self.request.user) | Q(user__in=followees)
        )
        queryset = self.filter_by_hashtags(queryset)
        return queryset

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user)
