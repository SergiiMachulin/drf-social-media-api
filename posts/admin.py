from typing import List

from django.contrib import admin
from django.db.models import Q, QuerySet

from posts.models import Post, Comment


class HashtagListFilter(admin.SimpleListFilter):
    title = "hashtags"
    parameter_name = "hashtags"

    def lookups(self, request, model_admin) -> List:
        queryset = Post.objects.all()
        hashtags_set = set()
        for post in queryset:
            hashtags = post.hashtags
            if hashtags is not None:
                for hashtag in hashtags.split("#"):
                    if hashtag:
                        hashtags_set.add(hashtag.strip())
        return [(hashtag, hashtag) for hashtag in sorted(hashtags_set)]

    def queryset(self, request, queryset) -> QuerySet:
        if self.value() is None:
            return queryset

        # Split the selected hashtag(s) into separate words
        hashtags = self.value().split("#")
        hashtags = [hashtag.strip() for hashtag in hashtags if hashtag.strip()]

        # Build a filter expression to match posts containing any of the selected hashtags
        q = Q()
        for hashtag in hashtags:
            q |= Q(hashtags__contains=f"#{hashtag}")

        return queryset.filter(q)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "content", "created_at")
    list_filter = (HashtagListFilter,)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "content", "created_at")
