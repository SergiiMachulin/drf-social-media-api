from django.contrib import admin

from posts.models import Post, Hashtag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "content", "created_at")
    list_filter = ("hashtags",)


@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

    class Meta:
        ordering = ["name"]
