from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User
from follower.models import Follower


class FollowInline(admin.TabularInline):
    model = Follower
    fk_name = "user"
    extra = 0
    verbose_name = "Followee"
    verbose_name_plural = "Followees"


class UserAdmin(BaseUserAdmin):
    inlines = [FollowInline]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "followers_count",
        "following_count",
    )
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("email", "first_name", "last_name", "email")
    ordering = ("-is_staff", "id", "email")

    def followers_count(self, obj):
        return obj.followers.select_related().count()

    def following_count(self, obj):
        return obj.followees.prefetch_related().count()

    followers_count.short_description = "Followed by you"
    following_count.short_description = "Follow you"


admin.site.register(User, UserAdmin)
