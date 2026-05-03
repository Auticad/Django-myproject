"""Serializers DRF — apps/api/serializers.py"""
from django.utils.text import slugify
from rest_framework import serializers
from apps.blog.models import Post, Category, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Tag
        fields = ['id', 'name', 'slug']


class CategorySerializer(serializers.ModelSerializer):
    post_count = serializers.IntegerField(read_only=True)

    class Meta:
        model  = Category
        fields = ['id', 'name', 'slug', 'post_count']


class PostListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(
        source='author.get_full_name', read_only=True
    )
    category    = CategorySerializer(read_only=True)
    tags        = TagSerializer(many=True, read_only=True)
    url         = serializers.HyperlinkedIdentityField(
        view_name='api:post-detail', lookup_field='slug'
    )

    class Meta:
        model  = Post
        fields = [
            'id', 'url', 'title', 'slug', 'excerpt',
            'author_name', 'category', 'tags',
            'status', 'views', 'created_at',
        ]


class PostDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(
        source='author.get_full_name', read_only=True
    )
    category    = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False,
        allow_null=True,
    )
    tags     = TagSerializer(many=True, read_only=True)
    tag_ids  = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        source='tags',
        many=True,
        write_only=True,
        required=False,
    )

    class Meta:
        model  = Post
        fields = [
            'id', 'title', 'slug', 'body', 'excerpt', 'cover',
            'author_name', 'category', 'category_id',
            'tags', 'tag_ids',
            'status', 'views', 'created_at', 'updated_at',
        ]
        read_only_fields = ['slug', 'author_name', 'views']

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError('Titolo troppo corto (min 5 caratteri).')
        return value.strip()

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        validated_data['slug']   = slugify(validated_data['title'])
        validated_data['author'] = self.context['request'].user
        post = Post.objects.create(**validated_data)
        post.tags.set(tags)
        return post

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tags is not None:
            instance.tags.set(tags)
        return instance
