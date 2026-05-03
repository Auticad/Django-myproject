"""ViewSet DRF — apps/api/views.py"""
from django.db.models import Count
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.blog.models import Post, Category, Tag
from .serializers import (
    PostListSerializer, PostDetailSerializer,
    CategorySerializer, TagSerializer,
)
from .permissions import IsAuthorOrReadOnly
from .filters import PostFilter


class PostViewSet(viewsets.ModelViewSet):
    queryset        = Post.published.all().select_related('author', 'category')
    lookup_field    = 'slug'
    filterset_class = PostFilter
    search_fields   = ['title', 'body', 'author__email']
    ordering_fields = ['created_at', 'views', 'title']
    ordering        = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        return PostDetailSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAuthorOrReadOnly()]
        return [permissions.AllowAny()]

    @action(
        detail=True,
        methods=['get'],
        url_path='related',
        permission_classes=[permissions.AllowAny],
    )
    def related(self, request, slug=None):
        post = self.get_object()
        related = Post.published.filter(
            category=post.category
        ).exclude(pk=post.pk)[:4]
        serializer = PostListSerializer(related, many=True, context={'request': request})
        return Response(serializer.data)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset        = Category.objects.annotate(post_count=Count('posts'))
    serializer_class = CategorySerializer
    lookup_field    = 'slug'


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset         = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field     = 'slug'
