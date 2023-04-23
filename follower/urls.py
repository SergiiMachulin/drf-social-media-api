from django.urls import path

from follower.views import FollowView, UnfollowView


urlpatterns = [
    path("follow/<int:pk>/", FollowView.as_view(), name="follow"),
    path("unfollow/<int:pk>/", UnfollowView.as_view(), name="unfollow"),
]

app_name = "follower"
