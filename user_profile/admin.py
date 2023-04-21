from django.contrib import admin

from user_profile.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "profile_picture", "bio")
    search_fields = ("user__username", "user__email")
