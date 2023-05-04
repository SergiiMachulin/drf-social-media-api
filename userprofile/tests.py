from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from .models import UserProfile
from .serializers import UserProfileSerializer


class UserProfileListTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="testpass"
        )
        self.client.force_authenticate(user=self.user)

    def test_user_profile_list(self):
        UserProfile.objects.create(user=self.user, bio="Test bio")
        response = self.client.get(reverse("profile:profile-list"))
        profiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(profiles, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_create_user_profile(self):
        data = {"bio": "Test bio"}
        response = self.client.post(reverse("profile:profile-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        profile = UserProfile.objects.get(user=self.user)
        serializer = UserProfileSerializer(profile)
        self.assertEqual(response.data, serializer.data)

    def test_create_existing_user_profile(self):
        UserProfile.objects.create(user=self.user, bio="Test bio")
        data = {"bio": "Test bio"}
        response = self.client.post(reverse("profile:profile-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserDetailProfileTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="testpass"
        )
        self.profile = UserProfile.objects.create(user=self.user, bio="Test bio")
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user_profile(self):
        response = self.client.get(reverse("profile:profile-detail"))
        serializer = UserProfileSerializer(self.profile)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_user_profile(self):
        data = {"bio": "New bio"}
        response = self.client.put(reverse("profile:profile-detail"), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["bio"], "New bio")

    def test_partial_update_user_profile(self):
        data = {"bio": "New bio"}
        response = self.client.patch(reverse("profile:profile-detail"), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["bio"], "New bio")

    def test_delete_user_profile(self):
        response = self.client.delete(reverse("profile:profile-detail"))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(UserProfile.objects.filter(user=self.user).exists())
