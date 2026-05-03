"""Test blog views e modelli — tests/test_blog.py"""
import pytest
from django.urls import reverse
from .factories import PostFactory, UserFactory, CategoryFactory


@pytest.mark.django_db
class TestPostListView:

    def test_returns_200(self, client):
        response = client.get(reverse('blog:post-list'))
        assert response.status_code == 200

    def test_shows_only_published(self, client):
        PostFactory.create_batch(3, status='published')
        PostFactory.create_batch(2, status='draft')
        response = client.get(reverse('blog:post-list'))
        assert response.context['posts'].count() == 3

    def test_search_filter(self, client):
        PostFactory(title='Django avanzato', status='published')
        PostFactory(title='Flask basilare', status='published')
        response = client.get(reverse('blog:post-list') + '?q=Django')
        assert response.context['posts'].count() == 1


@pytest.mark.django_db
class TestPostDetailView:

    def test_returns_200_for_published(self, client):
        post = PostFactory(status='published')
        response = client.get(reverse('blog:post-detail', kwargs={'slug': post.slug}))
        assert response.status_code == 200

    def test_returns_404_for_draft(self, client):
        post = PostFactory(status='draft')
        response = client.get(reverse('blog:post-detail', kwargs={'slug': post.slug}))
        assert response.status_code == 404

    def test_increments_views(self, client):
        post = PostFactory(status='published', views=0)
        client.get(reverse('blog:post-detail', kwargs={'slug': post.slug}))
        post.refresh_from_db()
        assert post.views == 1


@pytest.mark.django_db
class TestPostCreateView:

    def test_requires_login(self, client):
        response = client.get(reverse('blog:post-create'))
        assert response.status_code == 302

    def test_authenticated_user_can_access(self, client, django_user_model):
        user = django_user_model.objects.create_user(
            email='u@test.com', username='u', password='pass123'
        )
        client.login(email='u@test.com', password='pass123')
        response = client.get(reverse('blog:post-create'))
        assert response.status_code == 200


@pytest.mark.django_db
class TestPostAPI:

    def test_list_endpoint(self, api_client):
        PostFactory.create_batch(5, status='published')
        response = api_client.get('/api/posts/')
        assert response.status_code == 200
        assert response.data['count'] == 5

    def test_create_requires_auth(self, api_client):
        response = api_client.post('/api/posts/', {})
        assert response.status_code == 401

    def test_create_post_authenticated(self, auth_client):
        category = CategoryFactory()
        data = {
            'title':       'Test Post Titolo',
            'body':        'Contenuto del post di test.',
            'status':      'draft',
            'category_id': category.pk,
        }
        response = auth_client.post('/api/posts/', data, format='json')
        assert response.status_code == 201
        assert response.data['title'] == 'Test Post Titolo'
