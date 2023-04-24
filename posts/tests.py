from datetime import datetime
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory

from permissions.permissions import IsOwnerOrReadOnly
from posts.admin import PostAdmin, HashtagListFilter
from posts.models import Post
from posts.serializers import PostSerializer


class PostAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.factory = RequestFactory()
        self.post_admin = PostAdmin(Post, self.site)
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="testpass"
        )

    def test_hashtag_list_filter_lookups(self):
        # create test posts
        post1 = Post.objects.create(
            user=self.user,
            content="Test post with hashtags",
            hashtags="#hashtag1#hashtag2",
            created_at=datetime.now(),
        )
        post2 = Post.objects.create(
            user=self.user,
            content="Test post with hashtags",
            hashtags="#hashtag2#hashtag3",
            created_at=datetime.now(),
        )
        post3 = Post.objects.create(
            user=self.user,
            content="Test post with no hashtags",
            created_at=datetime.now(),
        )

        # create mock request object
        request = self.factory.get("/admin/posts/post/")
        request.user = self.user

        # get filter object and test lookups method
        filter = HashtagListFilter(request, {}, PostAdmin, Post)
        lookups = filter.lookups(request, self.post_admin)

        # assert expected values
        self.assertEqual(
            lookups,
            [
                ("hashtag1", "hashtag1"),
                ("hashtag2", "hashtag2"),
                ("hashtag3", "hashtag3"),
            ],
        )


class PostViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="testuser@test.com", password="testpass"
        )
        self.client.force_authenticate(user=self.user)
        self.post1 = Post.objects.create(user=self.user, content="Test post 1 content")
        self.post2 = Post.objects.create(user=self.user, content="Test post 2 content")
        self.post3 = Post.objects.create(user=self.user, content="Test post 3 content")

    def test_retrieve_post(self):
        url = reverse("posts:posts-detail", args=[self.post1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer_data = PostSerializer(self.post1).data
        self.assertEqual(response.data, serializer_data)

    def test_update_post(self):
        url = reverse("posts:posts-detail", args=[self.post1.id])
        data = {"content": "updated post", "hashtags": "#newhashtag"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post = Post.objects.get(id=response.data["id"])
        self.assertEqual(post.content, data["content"])
        self.assertEqual(post.hashtags, data["hashtags"])

    def test_delete_post(self):
        url = reverse("posts:posts-detail", args=[self.post1.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(pk=self.post1.pk).exists())


class IsOwnerOrReadOnlyTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="testuser@test.com", password="testpass"
        )
        self.post = Post.objects.create(user=self.user, content="Test content")
        self.client = APIClient()

    def test_owner_can_edit(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            reverse("posts:posts-detail", args=[self.post.pk]),
            {"content": "New test content"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_users_cannot_edit(self):
        response = self.client.patch(
            reverse("posts:posts-detail", args=[self.post.pk]),
            {"content": "New test content"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
