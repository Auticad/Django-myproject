"""URL API — apps/api/urls.py"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from . import views

app_name = 'api'

router = DefaultRouter()
router.register('posts',      views.PostViewSet,     basename='post')
router.register('categories', views.CategoryViewSet, basename='category')
router.register('tags',       views.TagViewSet,      basename='tag')

urlpatterns = router.urls + [
    # Auth JWT
    path('auth/token/',         TokenObtainPairView.as_view(),  name='token-obtain'),
    path('auth/token/refresh/', TokenRefreshView.as_view(),     name='token-refresh'),
    path('auth/token/verify/',  TokenVerifyView.as_view(),      name='token-verify'),
    # Documentazione OpenAPI
    path('schema/',   SpectacularAPIView.as_view(),                          name='schema'),
    path('docs/',     SpectacularSwaggerView.as_view(url_name='api:schema'), name='swagger'),
]
