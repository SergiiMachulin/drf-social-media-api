from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import UserProfileList, UserProfileDetail, UserProfileUpdate


urlpatterns = [
    path("", UserProfileList.as_view(), name="profile-list"),
    path("<int:pk>/", UserProfileDetail.as_view(), name="profile-detail"),
    path("<int:pk>/update/", UserProfileUpdate.as_view(), name="profile-update"),
]

app_name = "profile"
