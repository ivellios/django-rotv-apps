from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<slug>[\w_-]+)$', views.ShortenedURLRedirectView.as_view(), name='shortened-url-redirect'),
]
