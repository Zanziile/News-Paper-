# Generated by Django 4.1.5 on 2023-01-28 18:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0005_alter_comment_comment_text_subscribers'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='subscribers_category',
            field=models.ManyToManyField(through='news.Subscribers', to=settings.AUTH_USER_MODEL),
        ),
    ]
