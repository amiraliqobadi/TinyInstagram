from django.urls import path
from .views import (
    UserCreateView,
    SignInView,
    CustomLogoutView,
    CustomUserUpdateView,
    ChangePasswordView,
    AuthUserView,
)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("signup/", UserCreateView.as_view(), name="signup"),
    path("", SignInView.as_view(), name="signin"),
    path("logout/", login_required(CustomLogoutView.as_view()), name="logout"),
    path(
        "update/<int:pk>/",
        login_required(CustomUserUpdateView.as_view()),
        name="updateprofile",
    ),
    path(
        "passwordchange/",
        ChangePasswordView.as_view(),
        name="password_change",
    ),
    path(
        "activate/",
        AuthUserView.as_view(),
        name="activate_account",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
