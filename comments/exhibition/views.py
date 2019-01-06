from django.views import generic
from django.shortcuts import render

from archival.models import Article, Comment, User

def ArticleDetailView(request, **kwargs):
    data = {
        "article": Article.objects.get(pk=kwargs.get('pk')),
        "comments": Comment.objects.filter(article__ident=kwargs.get('pk'))
    }
    return render(request, 'exhibition/article_detail.html', data)

class ArticleListView(generic.ListView):
    template_name = 'exhibition/article_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.order_by('-published')[:30]

def UserDetailView(request, **kwargs):
    data = {
        "user": User.objects.get(pk=kwargs.get('uid'))
    }
    return render(request, 'exhibition/user_detail.html', data)

def ThreadListView(request, **kwargs):
    data = {
        "user": User.objects.get(pk=kwargs.get('uid')),
        "comments": Comment.objects.filter(author__uid=kwargs.get('uid'))
    }
    return render(request, 'exhibition/thread_detail.html', data)