from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=63, blank=True)
    last_name = models.CharField(max_length=63, blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_image", blank=True, null=True
    )
    bio = models.TextField(max_length=255, blank=True)
    location = models.CharField(max_length=50, blank=True)
    birthdate = models.DateField(null=True, blank=True)
