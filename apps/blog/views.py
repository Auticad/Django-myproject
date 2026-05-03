"""View blog — apps/blog/views.py"""

import logging

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import connection
from django.db.models import F, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import PostForm
from .models import Category, Post

logger = logging.getLogger("apps.blog")


# ─── Health Check ────────────────────────────────────────
def health_check(request):
    try:
        connection.ensure_connection()
        db_ok = True
    except Exception:
        db_ok = False

    status = 200 if db_ok else 503
    return JsonResponse(
        {
            "status": "ok" if db_ok else "degraded",
            "database": db_ok,
        },
        status=status,
    )


# ─── Blog Views ──────────────────────────────────────────
class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        qs = Post.published.all().select_related("author", "category")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(body__icontains=q))
        category_slug = self.request.GET.get("category")
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["search_query"] = self.request.GET.get("q", "")
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    slug_field = "slug"

    def get_object(self, queryset=None):
        obj = get_object_or_404(Post.published, slug=self.kwargs["slug"])
        Post.objects.filter(pk=obj.pk).update(views=F("views") + 1)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_posts"] = Post.published.filter(
            category=self.object.category
        ).exclude(pk=self.object.pk)[:3]
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post creato con successo.")
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user or self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, "Post aggiornato.")
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:post-list")

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user or self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, "Post eliminato.")
        return super().form_valid(form)


class CategoryDetailView(ListView):
    model = Post
    template_name = "blog/category_detail.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
        return Post.published.filter(category=self.category).select_related("author")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context


def about(request):
    User = get_user_model()

    stack = [
        {
            "layer": "Backend",
            "tech": "Django 5.2 LTS",
            "note": "Framework web Python full-stack",
        },
        {
            "layer": "Database",
            "tech": "PostgreSQL 16",
            "note": "Database relazionale principale",
        },
        {"layer": "Cache", "tech": "Redis 7", "note": "Cache e broker Celery"},
        {"layer": "API", "tech": "Django REST Framework", "note": "REST API con JWT"},
        {
            "layer": "Frontend",
            "tech": "Bootstrap 5 + HTMX",
            "note": "UI reattiva senza build step",
        },
        {
            "layer": "Deploy",
            "tech": "Docker + Nginx",
            "note": "Container production-ready",
        },
    ]

    authors = (
        User.objects.filter(posts__status="published")
        .distinct()
        .only("username", "first_name", "last_name", "bio", "avatar")
    )

    stats = {
        "post_count": Post.published.count(),
        "category_count": Category.objects.count(),
        "author_count": authors.count(),
    }

    return render(
        request,
        "about.html",
        {
            "stack": stack,
            "authors": authors,
            "stats": stats,
        },
    )
