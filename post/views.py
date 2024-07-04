from django.shortcuts import render, redirect
from django.views.generic import (
    ListView,
    TemplateView,
    DetailView,
    CreateView,
    UpdateView,
    View,
)
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import UploadForm
from .models import Post, Comments, Reply, Images
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from user.models import CustomUser
from django.shortcuts import get_object_or_404

class PostCreationView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "post/post.html"
    form_class = UploadForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.author = self.request.user
        images = self.request.FILES.getlist("images")
        images_list = []
        for image in images:
            file_path = default_storage.save(image.name, ContentFile(image.read()))
            images_list.append(file_path)
        post_images = Images.objects.create(images=json.dumps(images_list))
        form.instance.post_images = post_images
        return super().form_valid(form)

    def handle_no_permission(self):
        return redirect("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user.id
        try:
            user_post = Post.objects.filter(author=user)
        except Post.DoesNotExist:
            user_post = None
        if user_post is not None:
            for post in user_post:
                context["description"] = post.description
                context["date_posted"] = post.date_posted
                context["date_updated"] = post.date_updated
                context["author"] = post.author
                context["likes"] = post.likes
                context["post_view"] = post.views
                context = super().get_context_data(**kwargs)
        else:
            redirect("home")
            messages.error(self.request, "you dont have any posts yet!")
        return context


class ShowPostsView(ListView):
    model = Post
    template_name = 'post/show_post.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(author_id=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for post in context['posts']:
            post.is_liked = post.is_liked_by_user(self.request.user)
            

        register_user = CustomUser.objects.get(id=self.kwargs["pk"])
        
        context["register_user"] = register_user.profile_img
        context["register_user_name"] = register_user.user_name
        post_data = dict()
        for post in context['posts']:
            post_data[post] = json.loads(post.post_images.images)
        
        context["followers"] = register_user.followers.count()
        context["following"] = register_user.following.count()
        context["bio"] = register_user.bio
        context["posts_counter"] = Post.objects.filter(author_id=self.kwargs["pk"]).count()
        context["posts_images"] = post_data
        context["search_user"] = register_user
        
        posts_number = dict()
        post_comments = Comments.objects.filter(id=self.kwargs["pk"])
        

        
        

        
        return context
        
 
 
class JsonResponseMixin:
    def render_to_response(self, request, context, **response_kwargs):
        if self.request.is_ajax():
            return JsonResponse(context, safe=False, **response_kwargs)
        else:
            return super().render_to_response(context, **response_kwargs)
    

@method_decorator(csrf_exempt, name='dispatch')
class LikePostView(View):
    def post(self, request, *args, **kwargs):
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True
        post.save()
        return JsonResponse({'liked': liked, 'likes_count': post.number_of_likes()})


@method_decorator(login_required, name='dispatch')
class UnlikePostView(View):
    def post(self, request, *args, **kwargs):
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
            unliked = True
        else:
            unliked = False
        post.save()
        return JsonResponse({'unliked': unliked, 'likes_count': post.likes.count()})
    

@method_decorator(csrf_exempt, name='dispatch')
class CreateReplyView(View):
    def post(self, request, *args, **kwargs):
        comment_id = request.POST.get('comment_id')
        reply_text = request.POST.get('reply_text')
        user = request.user
        if not comment_id or not reply_text:
            return JsonResponse({'success': False, 'error': 'Missing comment_id or reply_text'})
        try:
            reply = Reply.objects.create(replys=reply_text, commnet_id=comment_id, user=user)
            return JsonResponse({'success': True, 'reply_id': reply.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


@method_decorator(csrf_exempt, name='dispatch')
class CreateCommentView(View):
    def post(self, request, *args, **kwargs):
        post_id = request.POST.get('post_id')
        comment_text = request.POST.get('comment_text')
        user = request.user

        post = get_object_or_404(Post, pk=post_id)

        if comment_text:
            comment = Comments.objects.create(text=comment_text, post_id=post, user=user)
            return JsonResponse({'success': True, 'comment_id': comment.id})
        else:
            return JsonResponse({'success': False, 'error': 'Missing comment_text'})