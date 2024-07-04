from django.urls import path
from .views import UserProfileView, DeletePostView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("profile/", login_required(UserProfileView.as_view()), name="profile"),
    path("delete_post/<int:pk>/", login_required(DeletePostView.as_view()), name="delete_post")
]
