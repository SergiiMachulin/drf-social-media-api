from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from permissions.permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    @action(detail=False)
    def following(self, request) -> Response:
        queryset = Post.objects.filter(user__followers=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        user = self.request.user
        queryset = Post.objects.filter(Q(user=user) | Q(user__in=user.following.all()))
        hashtags = self.request.query_params.get("hashtags")
        if hashtags:
            hashtags = hashtags.split(",")
            for hashtag in hashtags:
                queryset = queryset.filter(hashtags__contains=f"#{hashtag}")
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
