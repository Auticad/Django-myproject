"""Filtri DRF — apps/api/filters.py"""
import django_filters
from apps.blog.models import Post


class PostFilter(django_filters.FilterSet):
    title     = django_filters.CharFilter(lookup_expr='icontains')
    status    = django_filters.ChoiceFilter(choices=Post.STATUS_CHOICES)
    category  = django_filters.CharFilter(field_name='category__slug', lookup_expr='exact')
    tag       = django_filters.CharFilter(field_name='tags__slug',     lookup_expr='exact')
    date_from = django_filters.DateFilter(field_name='created_at',     lookup_expr='date__gte')
    date_to   = django_filters.DateFilter(field_name='created_at',     lookup_expr='date__lte')

    class Meta:
        model  = Post
        fields = ['status', 'category', 'tag']
