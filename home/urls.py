from django.urls import path
from .views import HomeView, FollowView, UnfollowView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("home/", login_required(HomeView.as_view()), name="home"),
    path("follow/<int:user_id>/", login_required(FollowView.as_view()), name="follow"),
    path(
        "unfollow/<int:user_id>/",
        login_required(UnfollowView.as_view()),
        name="unfollow",
    ),
]
