from django.conf.urls import patterns, include, url
from graphic import views


urlpatterns = patterns(
    '',
    (r'^$', views.data),
    (r'^data$', views.data),
    (r'^data/origin', views.list_all),
)
