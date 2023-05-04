from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from .models import Follower


class FollowerModelTestCase(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            email="user1@user.com", password="testpassword1"
        )
        self.user2 = get_user_model().objects.create_user(
            email="user2@user.com", password="testpassword2"
        )

    def test_follow(self):
        follow = Follower.objects.create(user=self.user1, followee=self.user2)
        self.assertEqual(Follower.objects.count(), 1)
        self.assertEqual(self.user1.following_set.count(), 1)
        self.assertEqual(self.user2.followers_set.count(), 1)
        self.assertEqual(str(follow), f"{self.user1} follows {self.user2}")

    def test_unfollow(self):
        Follower.objects.create(user=self.user1, followee=self.user2)
        self.assertEqual(Follower.objects.count(), 1)
        self.assertEqual(self.user1.following_set.count(), 1)
        self.assertEqual(self.user2.followers_set.count(), 1)
        follow = Follower.objects.get(user=self.user1, followee=self.user2)
        follow.unfollow()
        self.assertEqual(Follower.objects.count(), 0)
        self.assertEqual(self.user1.following_set.count(), 0)
        self.assertEqual(self.user2.followers_set.count(), 0)

    def test_duplicate_follow(self):
        Follower.objects.create(user=self.user1, followee=self.user2)
        with self.assertRaises(Exception):
            Follower.objects.create(user=self.user1, followee=self.user2)

    def test_follow_self(self):
        with self.assertRaises(Exception):
            Follower.objects.create(user=self.user1, followee=self.user1)

    def test_followed_at(self):
        follow = Follower.objects.create(user=self.user1, followee=self.user2)
        self.assertLess(follow.followed_at, timezone.now())


class FollowViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user3@user.com", password="testpassword3"
        )
        self.client.force_authenticate(user=self.user)
        self.followee = get_user_model().objects.create_user(
            email="user4@user.com", password="testpassword4"
        )

    def test_follow_user(self):
        url = reverse("follower:follow", kwargs={"pk": self.followee.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("Successfully followed.", response.data["detail"])
        self.assertTrue(
            Follower.objects.filter(user=self.user, followee=self.followee).exists()
        )

    def test_follow_self(self):
        url = reverse("follower:follow", kwargs={"pk": self.user.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("You cannot follow yourself.", response.data["detail"])
        self.assertFalse(
            Follower.objects.filter(user=self.user, followee=self.user).exists()
        )

    def test_follow_nonexistent_user(self):
        url = reverse("follower:follow", kwargs={"pk": 9999})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "The user with the specified ID does not exist.", response.data["detail"]
        )
        self.assertFalse(
            Follower.objects.filter(user=self.user, followee_id=9999).exists()
        )


class UnfollowViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user5@user.com", password="testpassword5"
        )
        self.client.force_authenticate(user=self.user)
        self.followee = get_user_model().objects.create_user(
            email="user6@user.com", password="testpassword6"
        )
        self.follower = Follower.objects.create(user=self.user, followee=self.followee)

    def test_unfollow_user(self):
        url = reverse("follower:unfollow", kwargs={"pk": self.followee.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Successfully unfollowed.", response.data["detail"])
        self.assertFalse(
            Follower.objects.filter(user=self.user, followee=self.followee).exists()
        )

    def test_unfollow_self(self):
        url = reverse("follower:unfollow", kwargs={"pk": self.user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("You cannot unfollow yourself.", response.data["detail"])
        self.assertFalse(
            Follower.objects.filter(user=self.user, followee=self.user).exists()
        )

    def test_unfollow_nonexistent_user(self):
        url = reverse("follower:unfollow", kwargs={"pk": 9999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Not found", response.data["detail"])
        self.assertFalse(
            Follower.objects.filter(user=self.user, followee_id=9999).exists()
        )
