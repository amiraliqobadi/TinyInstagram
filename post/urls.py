from django.urls import path
from .views import PostCreationView, ShowPostsView, LikePostView, UnlikePostView, CreateCommentView, CreateReplyView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("createpost/", login_required(PostCreationView.as_view()), name="createpost"),
    path("showposts/<int:pk>", login_required(ShowPostsView.as_view()), name="show_posts"),
    path('like_post/', LikePostView.as_view(), name='like_post'),
    path('unlike_post/', UnlikePostView.as_view(), name='unlike_post'),
    path('create_comment/', CreateCommentView.as_view(), name='create_comment'),
    path('create_reply/', CreateReplyView.as_view(), name='create_reply'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
