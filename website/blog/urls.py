from django.urls import path

from blog import views

app_name = "blog"
urlpatterns = [
    path(r'', views.IndexView.as_view(), name='index'),
]
