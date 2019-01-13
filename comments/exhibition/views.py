from django.db.models import Sum
from django.views import generic
from django.shortcuts import render
import markovify

from archival.models import Article, Comment, User

def ArticleDetailView(request, **kwargs):
    data = {
        "article": Article.objects.get(pk=kwargs.get('pk')),
        "comments": Comment.objects.filter(article__ident=kwargs.get('pk'))
    }
    return render(request, 'exhibition/article_detail.html', data)

def GeneratedDetailView(request, **kwargs):
    print('pk', kwargs.get('pk'))
    comments = {}
    all_comments = Comment.objects.filter(article=kwargs.get('pk'))
    comment_corpus = ""
    for comment in all_comments:
        comment_corpus += f'{comment.body}\n'
    text_model = markovify.NewlineText(comment_corpus)
    num_comments = 30
    data = {
        "article": Article.objects.get(pk=kwargs.get('pk')),
        "comments": [text_model.make_short_sentence(300) for num in range(num_comments)]
    }
    return render(request, 'exhibition/generated_detail.html', data)

class ArticleListView(generic.ListView):
    template_name = 'exhibition/article_list.html'
    context_object_name = 'articles'
    paginate_by = 30

    def get_queryset(self):
        return Article.objects.order_by('-published')

class PositiveArticleListView(generic.ListView):
    template_name = 'exhibition/article_list.html'
    context_object_name = 'articles'
    paginate_by = 30

    def get_queryset(self):
        return Article.objects.order_by('-comment_count')

def UserDetailView(request, **kwargs):
    data = {
        "user": User.objects.get(pk=kwargs.get('uid')),
        "karma": Comment.objects.filter(author__pk=kwargs.get('uid')).aggregate(karma=Sum('total_votes'))['karma']
    }
    return render(request, 'exhibition/user_detail.html', data)

def ThreadListView(request, **kwargs):
    data = {
        "user": User.objects.get(pk=kwargs.get('uid')),
        "comments": Comment.objects.filter(author__uid=kwargs.get('uid'))
    }
    return render(request, 'exhibition/thread_detail.html', data)