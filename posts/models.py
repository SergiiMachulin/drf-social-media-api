from django.db import models
from django.conf import settings


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to="post_image", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    hashtags = models.CharField(max_length=3000, default=None, null=True, blank=True)

    class Meta:
        default_related_name = "posts"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.content
