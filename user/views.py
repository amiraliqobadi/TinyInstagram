from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import request
from django.views.generic import (
    CreateView,
    UpdateView,
)
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django import forms
from django.views import View
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
import random
import string
from django.conf import settings
from django.templatetags.static import static
import datetime


class AuthUserView(View):
    template_name = "register/activate.html"
    success_url = reverse_lazy("signin")

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        if "email" in request.POST:
            user_email = request.POST.get("email")
            verification_code = self.generate_verification_code()
            self.send_verification_code(user_email, verification_code)
            request.session["user_email"] = user_email
            request.session["verification_code"] = verification_code
            return render(
                request, self.template_name, {"show_verification_code_input": True}
            )
        elif "verification_code" in request.POST:
            verification_code = request.POST.get("verification_code")
            stored_code = request.session.get("verification_code")
            if verification_code == stored_code:
                user_email = request.session.get("user_email")
                try:
                    user = CustomUser.objects.get(email=user_email)
                    user.is_active = True
                    if "profile_img" in self.request.FILES:
                        User.profile_img = self.request.FILES["profile_img"]
                    else:
                        User.profile_img = static("default-avatar.png")
                    user.save()
                    messages.success(request, "Account activated successfully!")
                except CustomUser.DoesNotExist:
                    messages.error(request, "User with this email does not exist.")
                return HttpResponseRedirect(self.success_url)
            else:
                messages.error(request, "Invalid verification code. Please try again.")
        return render(request, self.template_name)

    @staticmethod
    def generate_verification_code():
        return "".join(random.choices(string.digits, k=6))

    @staticmethod
    def send_verification_code(user_email, verification_code):
        subject = "Authentication code: Tiny Instagram"
        message = f"Your authentication code is: {verification_code}"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])


class UserCreateView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "register/signup.html"
    success_url = reverse_lazy("activate_account")

    def form_valid(self, form):
        User.is_active = False
        form.save(commit=False)
        return super().form_valid(form)


class SignInView(LoginView):
    template_name = "register/signin.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        messages.success(self.request, "Login successful. Welcome back!")
        return super().form_valid(form)


class CustomLogoutView(LogoutView, LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        CustomUser.last_login = datetime.datetime.now()
        redirect("signin")
        return super().dispatch(request, *args, **kwargs)

    def get_next_page(self):
        return reverse_lazy("signin")


class CustomUserUpdateView(UpdateView, LoginRequiredMixin, forms.ModelForm):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "register/update.html"
    success_url = reverse_lazy("home")
    pk_url_kwarg = "pk"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pk=self.kwargs["pk"])

    def form_valid(self, form):
        if form.cleaned_data.get("profile_img-clear"):
            if self.object.profile_img:
                self.object.profile_img.delete(save=False)
                messages.success(self.request, "Your profile image removed")
                self.object.profile_img = None
        messages.success(self.request, "Your information has been updated successfully")
        return super().form_valid(form)


class ChangePasswordView(PasswordChangeView, LoginRequiredMixin):
    form_class = PasswordChangeForm
    template_name = "register/password_change_form.html"
    success_url = reverse_lazy("signin")
