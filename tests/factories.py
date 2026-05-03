"""Factory Boy factories — tests/factories.py"""
import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model
from apps.blog.models import Post, Category, Tag

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email    = factory.LazyAttribute(lambda o: f'{o.username}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')
    is_active = True


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker('word', locale='it_IT')
    slug = factory.LazyAttribute(lambda o: o.name.lower().replace(' ', '-'))


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Faker('word', locale='it_IT')
    slug = factory.LazyAttribute(lambda o: o.name.lower())


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    title    = factory.Faker('sentence', nb_words=6, locale='it_IT')
    slug     = factory.LazyAttribute(
        lambda o: o.title.lower().replace(' ', '-').replace('.', '')[:50]
    )
    body     = factory.Faker('paragraphs', nb=5, locale='it_IT')
    excerpt  = factory.Faker('paragraph', locale='it_IT')
    author   = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    status   = 'published'
