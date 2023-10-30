# from datetime import date
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse
from .models import Post
from django.views.generic import ListView, DetailView
from .forms import CommentForm
from django.views import View
from django.http import HttpResponseRedirect

all_posts = []


# def get_date(post):
#     return post["date"]
# sorted_posts = sorted(all_posts, key=get_date)


# Create your views here.


# def starting_page(request):
#     latest_posts = Post.objects.all().order_by("-date")[:3]
#     return render(request, "blog/index.html", {"posts": latest_posts})


class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        data = queryset[:3]
        return data


# def posts(request):
#     posts = Post.objects.all().order_by("-date")
#     return render(request, "blog/all-posts.html", {"all_posts": posts})


class AllPostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"


class SinglePostView(View):
    template_name = "blog/post-detail.html"

    def get_context(post, request, CommentForm=CommentForm()):
        print(post.tags.all())
        stored_posts = request.session.get("stored_posts")
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm,
            "comments": post.comments.all().order_by("-id"),
            "is_saved_for_later": stored_posts is not None and post.id in stored_posts,
        }
        return context

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        return render(
            request,
            SinglePostView.template_name,
            SinglePostView.get_context(post, request),
        )

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))
        return render(
            request,
            SinglePostView.template_name,
            SinglePostView.get_context(post, request, comment_form),
        )


# class SinglePostView(DetailView):
#     template_name = "blog/post-detail.html"
#     model = Post

#     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
#         context = super().get_context_data(**kwargs)
#         context["tags"] = self.object.tags.all()
#         context["comment_form"] = CommentForm
#         return context


# def post_detail(request, slug):
#     # identified_post = next(post for post in posts if post["slug"] == slug)
#     identified_post = Post.objects.get(slug=slug)
#     return render(
#         request,
#         "blog/post-detail.html",
#         {
#             "post": identified_post,
#             "tags": identified_post.tags.all(),
#         },
#     )


class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")
        context = {}
        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True
        return render(request, "blog/stored-posts.html", context)

    def post(self, request):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is None:
            stored_posts = []
        post_id = int(request.POST["post_id"])
        
        if post_id not in stored_posts:
            stored_posts.append(post_id)
            request.session["stored_posts"] = stored_posts
            return HttpResponseRedirect("/")
        stored_posts.remove(post_id)
        request.session["stored_posts"] = stored_posts
        return HttpResponseRedirect("/")
