"""Modelli blog — apps/blog/models.py"""
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.db.models import Count


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nome')
    slug = models.SlugField(max_length=110, unique=True)

    class Meta:
        verbose_name        = 'Categoria'
        verbose_name_plural = 'Categorie'
        ordering            = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category-detail', kwargs={'slug': self.slug})


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Tag')
    slug = models.SlugField(max_length=60, unique=True)

    class Meta:
        verbose_name        = 'Tag'
        verbose_name_plural = 'Tag'
        ordering            = ['name']

    def __str__(self):
        return self.name


class PublishedManager(models.Manager):
    """Manager che restituisce solo i post pubblicati."""
    def get_queryset(self):
        return super().get_queryset().filter(status='published')

    def with_stats(self):
        return self.get_queryset().annotate(tag_count=Count('tags'))


class Post(models.Model):
    STATUS_CHOICES = [
        ('draft',     'Bozza'),
        ('published', 'Pubblicato'),
    ]

    title    = models.CharField(max_length=200, verbose_name='Titolo')
    slug     = models.SlugField(max_length=220, unique=True)
    body     = models.TextField(verbose_name='Contenuto')
    excerpt  = models.TextField(blank=True, verbose_name='Estratto')
    cover    = models.ImageField(
        upload_to='posts/covers/%Y/%m/',
        blank=True,
        verbose_name='Copertina',
    )
    status   = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name='Stato',
        db_index=True,
    )
    views    = models.PositiveIntegerField(default=0, verbose_name='Visualizzazioni')

    author   = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Autore',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='Categoria',
    )
    tags = models.ManyToManyField(
        Tag, blank=True, related_name='posts', verbose_name='Tag'
    )

    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    objects   = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name        = 'Post'
        verbose_name_plural = 'Post'
        ordering            = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['author', 'status']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post-detail', kwargs={'slug': self.slug})
