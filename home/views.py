from django.shortcuts import render
from user.models import CustomUser
from django.views.generic import ListView, TemplateView
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from post.forms import UploadForm
from post.models import Post
from django.db.models import Q
import json
from .filters import UserFilter
from django.http import JsonResponse
from django.views import View
from user.models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.contrib import messages


class FollowView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        try:
            user_to_follow = CustomUser.objects.get(pk=user_id)
            request.user.follow(user_to_follow)
            messages.success(self.request, f"{self.request.user.username} user followed")
            return JsonResponse(
                {"status": "success", "message": "You have followed the user."}
            )
        except CustomUser.DoesNotExist:
            messages.error(self.request, "user dos'nt exist")
            return JsonResponse(
                {"status": "error", "message": "User not found"}, status=404
            )


class UnfollowView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        try:
            user_to_unfollow = CustomUser.objects.get(pk=user_id)
            request.user.unfollow(user_to_unfollow)
            messages.success(self.request, "This user unfollowed")
            return JsonResponse(
                {"status": "success", "message": "You have unfollowed the user."}
            )
        except CustomUser.DoesNotExist:
            messages.error(self.request, "user dos'nt exist")
            return JsonResponse(
                {"status": "error", "message": "User not found"}, status=404
            )


class HomeView(ListView):
    template_name = "home/home.html"
    model = CustomUser

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("user_name")
        if query:
            user_filter = UserFilter(self.request.GET, queryset=queryset)
            return user_filter.qs
        else:
            return queryset.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        RegisterUser = self.request.user
        if RegisterUser.is_authenticated:
            if RegisterUser.profile_img:
                context["profile_img"] = RegisterUser.profile_img
            posts = RegisterUser.posts.all()
            context["posts"] = posts
            if posts.count() == 0:
                context["posts_images"] = None
            else:
                post_data = {}
                for post in posts:
                    post_data[post] = json.loads(post.post_images.images)
                context["posts_images"] = post_data

            context["postscounter"] = posts.count()
            context["followers"] = RegisterUser.followers.count()
            context["following"] = RegisterUser.following.count()
            context["bio"] = RegisterUser.bio
            context["filter"] = UserFilter(
                self.request.GET,
                queryset=self.get_queryset(),
            )
        return context
