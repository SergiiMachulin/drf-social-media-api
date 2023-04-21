from django.db import models
from django.conf import settings


class Hashtag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to="post_image", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    hashtags = models.ManyToManyField(Hashtag, blank=True)

    class Meta:
        default_related_name = "posts"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.content
