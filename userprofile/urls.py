from django.urls import path

from .views import UserProfileList, UserDetailProfile

urlpatterns = [
    path("profiles/", UserProfileList.as_view(), name="profile-list"),
    path("profile/", UserDetailProfile.as_view(), name="profile-detail"),
]

app_name = "profile"
