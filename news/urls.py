from django.urls import path
from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, Subscribe, Success, Categories, IndexView

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('articles/create/', PostCreate.as_view(), name='post_create'),
    path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('category/<int:pk>', Subscribe.as_view(), name='subscribe'),
    path('category/<int:pk>/success', Success.as_view(), name='success'),
    path('category/', Categories.as_view(), name='subscribe'),
]
