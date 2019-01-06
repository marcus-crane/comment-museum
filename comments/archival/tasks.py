from celery import shared_task
from django.conf import settings
import os
import requests
import pendulum

from archival.models import Article, Comment, User

@shared_task
def fetch_streams():
    r = requests.get(settings.STREAM_URL)
    data = r.json()
    for stream in data['streams']:
        created_ms = stream.get('createDate') / 1000
        created_ts = pendulum.from_timestamp(created_ms, 'NZ').to_w3c_string()
        try:
            Article.objects.create(
                ident=stream.get('streamID'),
                url=stream.get('streamURL'),
                title=stream.get('streamTitle'),
                comment_count=stream.get('commentCount'),
                published=created_ts,
            )
        except:
            print(f"Article already exists, skipping {stream.get('streamID')}")

@shared_task
def fetch_comments():
    streams = Article.objects.order_by('-updated')
    for stream in streams:
        print(f'Starting {stream.title}')
        r = requests.get(settings.COMMENTS_URL.format(stream.ident))
        data = r.json()
        for comment in data['comments']:
            sender = comment['sender']
            if sender['name'] == '[removed]' or comment['status'] == 'deleted':
                print('Skipping deleted thread')
                continue
            print(f"comment by {sender['UID']}: {sender['name']}")
            try:
                user = User.objects.get(pk=sender['UID'])
            except:
                user = User.objects.create(
                    uid=sender.get('UID'),
                    avatar=sender.get('photoURL'),
                    name=sender.get('name'),
                    url=sender.get('profileURL', 'https://stuff.co.nz'),
                    login_provider=sender.get('loginProvider'),
                    moderator=comment.get('isModerator')
                )
            created_ms = comment.get('timestamp') / 1000
            created_ts = pendulum.from_timestamp(created_ms, 'NZ').to_w3c_string()
            Comment.objects.create(
                ident=comment.get('ID'),
                article=stream,
                thread_id=comment.get('threadID', False),
                parent_id=comment.get('parentID', False),
                body=comment.get('commentText'),
                total_votes=comment.get('TotalVotes'),
                upvotes=comment.get('posVotes'),
                downvotes=comment.get('negVotes'),
                created=created_ts,
                author=user
            )