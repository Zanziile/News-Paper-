from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
from .models import Post
from NewsPaper.settings import DEFAULT_FROM_EMAIL


@receiver(m2m_changed, sender=Post.category.through, dispatch_uid='notify_post_created_signal')
def notify_post(sender, instance, action, **kwargs):
    if action == 'post_add':
        senders = []
        for category in instance.category.all():
            for subscriber in category.subscribers_category.all():
                senders.append(subscriber.email)

        html_content = render_to_string('email.html', {'post': instance})
        msg = EmailMultiAlternatives(
            subject=f'{instance}',
            body='',
            from_email=DEFAULT_FROM_EMAIL,
            to=senders
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
