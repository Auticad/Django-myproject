"""Root URLconf — config/urls.py"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.blog.views import health_check


urlpatterns = [
    path('admin/',    admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('blog/',     include('apps.blog.urls', namespace='blog')),
    path('api/',      include('apps.api.urls',  namespace='api')),
    path('health/',   health_check, name='health'),
    path('',          include('apps.blog.urls', namespace='blog_root')),
]

# Media files in sviluppo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
