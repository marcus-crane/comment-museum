from django.urls import path

from . import views

app_name = 'exhibition'
urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article_list'),
    path('article/<path:pk>', views.ArticleDetailView, name='article_detail'),
    path('user/<int:uid>', views.UserDetailView, name='user_detail.html'),
    path('threads/<int:uid>', views.ThreadListView, name="thread_detail.html"),
    path('positive/', views.PositiveArticleListView.as_view(), name='positive_article_list'),
    path('generated/<path:pk>', views.GeneratedDetailView, name='generated_detail'),
]