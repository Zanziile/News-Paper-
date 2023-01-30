from celery import shared_task
from datetime import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from NewsPaper.settings import *

from .models import Post, Category

@shared_task
def mail_new():
    post = Post.save(commit=False)
    html_content = render_to_string(
        'email.html',
        {
            'post': post,
            'text': post.preview,
            'link': f'http://127.0.0.1:8000/news/{post.pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'{post.title}',
        body=post.body,
        from_email=DEFAULT_FROM_EMAIL,
        to=Category.subscribers_category
    )
    msg.attach_alternative(html_content, "text/html")

    msg.send()

@shared_task
def week_news_notification():
    for category in Category.subscribers_category.all():
        senders = []
        for subscriber in category.subscribers_category.all():
            senders.append(subscriber.email)

        html_content = render_to_string('email_week.html', {'posts': Post.category.filter(categories=category).filter(
            create_time__lt=datetime.now() - timedelta(days=7))})
        msg = EmailMultiAlternatives(
            subject=f'Список новых статей за прошедшую неделю!',
            body='',
            from_email='DEFAULT_FROM_EMAIL',
            to=senders
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
