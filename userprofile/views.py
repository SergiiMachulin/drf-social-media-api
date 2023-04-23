from typing import Any

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics, filters
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from .models import UserProfile
from permissions.permissions import IsOwnerOrReadOnly
from .serializers import UserProfileSerializer


class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["user__email"]

    @extend_schema(
        parameters=[OpenApiParameter(name="search", type=str, required=False)],
        description="List all user profiles with optional search by email",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(description="Create a new user profile")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @extend_schema(description="Create a new user profile")
    def perform_create(self, serializer) -> Any:
        user_profile = UserProfile.objects.filter(user=self.request.user)
        if user_profile.exists():
            raise ValidationError("User profile already exists")
        serializer.save(user=self.request.user)


class UserDetailProfile(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    @extend_schema(description="Retrieve a user profile")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(description="Update a user profile")
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(description="Partial update a user profile")
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(description="Delete a user profile")
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_object(self) -> Any:
        obj = get_object_or_404(self.queryset, user=self.request.user)
        return obj
