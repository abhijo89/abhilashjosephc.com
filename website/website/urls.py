from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path(r'', TemplateView.as_view(template_name='base.html'), name='index'),
                  path(r'blog/', include('blog.urls', namespace='blog')),
                  path(r'blog/', include('comments.urls', namespace='comment')),
                  path(r'blog/', include('accounts.urls', namespace='account')),
                  path(r'blog/', include('oauth.urls', namespace='oauth')),
    path('admin/', admin.site.urls),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
