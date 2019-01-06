from django.contrib import admin

from archival.models import Article, Comment, User

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'comment_count', 'published', 'updated')
    list_filter = ['published', 'expired']
    search_fields = ['ident', 'title', 'url']

class CommentAdmin(admin.ModelAdmin):
    list_display = ('created', 'author', 'body', 'total_votes')
    list_filter = ['deleted']
    search_fields = ['body', 'ident']

class UserAdmin(admin.ModelAdmin):
    list_display = ('uid', 'name', 'login_provider')
    list_filter = ['moderator', 'login_provider']
    search_fields = ['avatar', 'name', 'url']
    

admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(User, UserAdmin)