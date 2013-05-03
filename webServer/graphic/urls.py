from django.conf.urls import patterns, include, url
from graphic import views


urlpatterns = patterns(
    '',
    (r'^$', views.init),
    (r'^data$', views.data),
)
