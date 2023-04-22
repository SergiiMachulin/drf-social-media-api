from rest_framework import generics, filters
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import UserProfile
from permissions.permissions import IsOwnerOrReadOnly
from .serializers import UserProfileSerializer


class UserProfileList(generics.ListCreateAPIView):
    """With search functionality using case-insensitive partial matches by email"""

    queryset = UserProfile.objects
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["user__email"]

    def perform_create(self, serializer):
        user_profile = UserProfile.objects.filter(user=self.request.user)
        if user_profile.exists():
            raise ValidationError("User profile already exists")
        serializer.save(user=self.request.user)


class UserProfileDetail(generics.RetrieveAPIView):
    queryset = UserProfile.objects
    serializer_class = UserProfileSerializer


class UserProfileUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        obj = get_object_or_404(self.queryset, user=self.request.user)
        return obj
