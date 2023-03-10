from django_filters import FilterSet
from .models import Post


class NewsFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
         'title': ['icontains'],
         'post_choice': ['icontains'],
         'create_time': []
        }
