from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    user_name = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)

    def user_rate_update(self):
        self.user_rating = 0
        for post in Post.objects.filter(user_name=self):
            self.user_rating += post.post_rating * 3
            for comment in Comment.objects.filter(comment_post=post):
                self.user_rating += comment.comment_rating
        for comment in Comment.objects.filter(comment_user=self.user_name):
            self.user_rating += comment.comment_rating
        self.save()

    def __str__(self):
        return f'{self.user_name}'


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    subscribers_category = models.ManyToManyField(User, through='Subscribers')

    def __str__(self):
        return f'{self.category_name}'


class Post(models.Model):
    news = 'Новости'
    articles = 'Статьи'
    POST_CHOICES = [
        ("Новости", 'News'),
        ("Статьи", 'Articles')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_choice = models.CharField(max_length=255, choices=POST_CHOICES, default=articles)
    create_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through="PostCategory")
    title = models.CharField(max_length=255, unique=True)
    body = models.TextField()
    post_rating = models.IntegerField(default=0)

    def preview(self):
        self.body = self.body[0:125] + '...'
        self.save()

    def post_like(self, amount=1):
        self.post_rating += amount
        self.save()

    def post_dislike(self, amount=1):
        self.post_rating -= amount
        self.save()

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.title}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_name = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(default='Без текста')
    comment_time = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def comment_like(self, amount=1):
        self.comment_rating += amount
        self.save()

    def comment_dislike(self, amount=1):
        self.comment_rating -= amount
        self.save()


class Subscribers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category_subscribers = models.ForeignKey(Category, on_delete=models.CASCADE)
