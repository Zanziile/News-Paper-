from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Subscribers
from .forms import PostForm
from .filters import NewsFilter
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import redirect


class Subscribe(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'subscribe.html'
    context_object_name = 'subscribe'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        usercategory = Subscribers(
            user=self.request.user,
            category_subscribers=self.get_object()
        )
        usercategory.save()
        return redirect(f'/news/category/{self.get_object().id}/success')


class PostList(ListView):
    model = Post
    ordering = 'create_time'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = 'news.post_create'


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)

        if 'news' in self.request.path.split('/'):
            post.post_choice = 'News'
            self.success_url = reverse_lazy('news_list')
        else:
            post.post_choice = 'Articles'
            self.success_url = reverse_lazy('articles_list')
        return super().form_valid(form)


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        post = form.save(commit=False)

        if 'news' in self.request.path.split('/'):
            post.post_choice = 'Новости'
            self.success_url = reverse_lazy('post_list')
        else:
            post.post_choice = 'Статьи'
            self.success_url = reverse_lazy('articles_list')
        return super().form_valid(form)


class Success(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'success.html'
    context_object_name = 'success'


class Categories(ListView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'category'
