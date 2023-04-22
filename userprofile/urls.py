from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import UserProfileList, UserProfileDetail, UserProfileUpdate


urlpatterns = [
    path("", UserProfileList.as_view(), name="profile-list"),
    path("<int:pk>/", UserProfileDetail.as_view(), name="profile-detail"),
    path("update/", UserProfileUpdate.as_view(), name="profile-update"),
]

urlpatterns += format_suffix_patterns(
    [
        path("", UserProfileList.as_view(), name="profile-list"),
    ]
)


app_name = "profile"
