from django.shortcuts import render, redirect
from django.views.generic import (
    ListView,
    DeleteView,
)
from post.models import Post
from user.models import CustomUser
from django.urls import reverse_lazy
from .forms import FormDeleteUser
from django.views.generic.edit import FormMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import check_password
from django.templatetags.static import static
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.http import HttpResponseRedirect


class UserProfileView(FormMixin, ListView, LoginRequiredMixin):
    template_name = "userprofile/userprofile.html"
    model = Post
    success_url = reverse_lazy("signup")
    form_class = FormDeleteUser

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        RegisterUser = self.request.user
        if form.is_valid():
            user = _(form.cleaned_data["user_name"])
            password = _(form.cleaned_data["password"])

            if user == self.request.user.user_name and check_password(
                password, self.request.user.password
            ):
                RegisterUser.delete()
                return redirect("signup")
            else:
                messages.error(self.request, "Check your user name and password")
                return redirect("profile")
        else:
            messages.error(self.request, "Sth went wrong")
            return redirect("profile")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        RegisterUser = self.request.user
        if self.request.user.is_authenticated:

            if RegisterUser.profile_img:
                context["profile_img"] = RegisterUser.profile_img

            user_info = dict()
            followers_with_images = self.request.user.get_followers_with_images()
            for follower in followers_with_images:
                user_info[follower['user_name']] = follower['profile_img']
            if not user_info:
                context["followers_info"] = "you dont have follower"
            else:
                context["followers_info"] = user_info

            following = dict()
            following_info = self.request.user.get_following_info()
            for user in following_info:
                following[user['user_name']] = {
                    'profile_img': user['profile_img'],
                    'last_login': user['last_login'],
                    'bio': user['bio']
                }
                print(user['profile_img'])
            if not following_info:
                context["following_info"] = "you should follow some body"
            else:
                context["following_info"] = following

            if RegisterUser.posts.all().count() == 0:
                context["posts"] = None
            else:
                context["posts"] = self.request.user.posts.all()
                post_data = {}
                for post in RegisterUser.posts.all():
                    post_data[post] = json.loads(post.post_images.images)[0]
                context["posts_images"] = post_data
            context["postscounter"] = self.request.user.posts.all().count()

        return context


class DeletePostView(DeleteView):
    model = Post
    template_name = "userprofile/userprofile.html"
    pk_url_kwarg = "pk"
    success_url = reverse_lazy("profile")
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pk=self.kwargs["pk"])
    
    def form_valid(self, form):
        if form.cleaned_data:
            if self.object.post_img:
                self.object.post_img.delete(save=False)
                messages.success(self.request, "Your post removed removed")
                self.object.profile_img = None
        return super().form_valid(form)
    

   
    

        
    
   
    
        
