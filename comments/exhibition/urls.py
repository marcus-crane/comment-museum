from django.urls import path

from . import views

app_name = 'exhibition'
urlpatterns = [
    path('', views.StreamView.as_view(), name='stream_list'),
]