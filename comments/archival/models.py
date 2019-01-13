from django.db import models

class Article(models.Model):
    ident = models.CharField(max_length=40, primary_key=True)
    url = models.URLField()
    title = models.TextField()
    comment_count = models.IntegerField()
    scraped = models.DateTimeField(auto_now_add=True)
    published = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)
    expired = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Comment(models.Model):
    ident = models.CharField(max_length=40, primary_key=True)
    article = models.ForeignKey('Article', on_delete=models.CASCADE,)
    thread_id = models.CharField(max_length=40)
    parent_id = models.CharField(max_length=40)
    body = models.TextField()
    total_votes = models.IntegerField()
    upvotes = models.IntegerField()
    downvotes = models.IntegerField()
    created = models.DateTimeField()
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.body

class User(models.Model):
    uid = models.CharField(max_length=40, primary_key=True)
    avatar = models.URLField()
    name = models.TextField()
    url = models.URLField()
    login_provider = models.CharField(max_length=40)
    moderator = models.BooleanField(default=False)

    def __str__(self):
        return self.name


