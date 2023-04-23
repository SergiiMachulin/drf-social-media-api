from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Follower(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="following_set",
    )
    followee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followers_set",
    )
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "followee"]

    def __str__(self) -> str:
        return f"{self.user} follows {self.followee}"

    def clean(self):
        if self.user == self.followee:
            raise ValidationError("Cannot follow oneself.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def unfollow(self):
        self.delete()
