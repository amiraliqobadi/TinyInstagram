from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    is_verified = models.BooleanField(default=False)
    email = models.EmailField(_("email address"))
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True, auto_now=True)
    user_name = models.CharField(_("user name"), max_length=255, unique=True)
    first_name = models.CharField(_("first name"), max_length=255, blank=True)
    last_name = models.CharField(_("last name"), max_length=255, blank=True)
    bio = models.TextField(blank=True)
    following = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="followers",
        blank=True,
    )
    profile_img = models.ImageField(
        upload_to="images/profile_images",
        blank=True,
    )
    USERNAME_FIELD = "user_name"
    objects = CustomUserManager()

    def __str__(self):
        return self.user_name

    def count_followers(self):
        return self.followers.count()

    def count_following(self):
        return self.following.count()

    def follow(self, user):
        if not self.is_following(user):
            self.following.add(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)

    def is_following(self, user):
        return self.following.filter(pk=user.pk).exists()

    def get_following(self):
        return self.following.all()

    def get_followers(self):
        return self.followers.all()

    def get_followers_with_images(self):
        return self.followers.all().values('user_name', 'profile_img')

    def get_following_info(self):
        return self.following.all().values('user_name', 'profile_img', "last_login", "bio")
