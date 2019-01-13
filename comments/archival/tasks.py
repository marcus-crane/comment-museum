from celery import shared_task
from django.conf import settings
import os
import requests
import pendulum
from bs4 import BeautifulSoup

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'museum.settings')

import django
django.setup()

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
            pass

@shared_task
def fetch_articles(date):
    results = []
    def query_page(date, page=1):
        r = requests.get(settings.ARCHIVE_URL.format(date, page))
        soup = BeautifulSoup(r.text, 'html.parser')
        links = soup.find_all("p", class_="archive-listing-item")
        for link in links:
            results.append(link.a['href'])
        paginator = soup.find('div', 'archive-listing-bottom')
        if 'Next' in paginator.find_all('span')[-1].get_text():
            query_page(date, page+1)
    query_page(date)
    for result in results:
        metadata = determine_metadata(result)
        
    
def determine_metadata(link):
    body = link.replace('https://www.stuff.co.nz', '').replace('https://i.stuff.co.nz', '')
    metadata = body.split('/')[1:-1]
    if len(metadata) == 2:
        print({'category': metadata[0], 'ident': metadata[1]})
    if len(metadata) == 3:
        print({'category': metadata[0], 'bicategory': metadata[1], 'ident': metadata[2]})
    if len(metadata) == 4:
        print({'category': metadata[0], 'bicategory': metadata[1], 'tricategory': metadata[2], 'ident': metadata[3]})


@shared_task
def fetch_comments():
    streams = Article.objects.order_by('-updated')
    for stream in streams:
        r = requests.get(settings.COMMENTS_URL.format(stream.ident))
        data = r.json()
        for comment in data['comments']:
            sender = comment['sender']
            if sender['name'] == '[removed]' or comment['status'] == 'deleted':
                try:
                    del_comment = Comment.objects.get(pk=comment.get('ID'))
                    del_comment.deleted = True
                    del_comment.save()
                    print(f'Updated deleted comment: {comment.body}')
                except:
                    print('Skipping deleted thread')
                    continue
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
            try:
                Comment.objects.get(pk=comment.get('ID'))
            except:
                print(f"Importing {comment.get('ID')}")
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