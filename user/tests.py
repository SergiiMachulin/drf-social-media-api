from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from user.models import User


class UserViewsTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )
        self.token = str(AccessToken.for_user(self.user))

    def test_create_user(self):
        url = reverse("user:create")
        data = {
            "email": "newuser@example.com",
            "password": "newpassword",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.data.get("email"), "newuser@example.com")

    def test_retrieve_user(self):
        url = reverse("user:manage")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("email"), "testuser@example.com")

    def test_update_user(self):
        url = reverse("user:manage")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        data = {"first_name": "John", "last_name": "Doe"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.last_name, "Doe")

    def test_list_user_followers(self):
        url = reverse("user:user_followers")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        self.assertEqual(len(response.data["results"]), 0)

    def test_list_user_following(self):
        url = reverse("user:user_following")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)
