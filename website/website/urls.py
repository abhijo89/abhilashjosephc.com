from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path(r'', TemplateView.as_view(template_name='base.html'), name='index'),
    path('admin/', admin.site.urls),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
