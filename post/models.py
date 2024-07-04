from django.db import models
from user.models import CustomUser
from django.core.validators import MinValueValidator
from django.conf import settings


class Images(models.Model):
    images = models.TextField()


class Post(models.Model):
    post_images = models.ForeignKey(
        Images,
        on_delete=models.CASCADE,
        related_name="post_images",
    )
    description = models.TextField(blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    views = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    likes = models.ManyToManyField(CustomUser, related_name='liked_posts', blank=True)
    saves = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    comments = models.IntegerField(validators=[MinValueValidator(0)], default=0)

    def number_of_likes(self):
        return self.likes.count()
    
    def is_liked_by_user(self, user):
        return self.likes.filter(id=user.id).exists()


class Comments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    date_comment = models.DateTimeField(auto_now_add=True)
    date_edit = models.DateField(auto_now=True)
    post_id = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments_set",
    )
    



class Reply(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    replys = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_edit = models.DateField(auto_now=True)
    commnet = models.ForeignKey(
        Comments,
        on_delete=models.CASCADE,
        related_name="replys_set",
    )
