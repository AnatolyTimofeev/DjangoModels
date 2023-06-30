# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from .tasks import send_email_task
from django.core.cache import cache

from django.shortcuts import redirect, render
from .signals import postlimit, limit_post_signal

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,FormView

from .forms import NewsForm, CatForms
from .models import Post, Category, Author
from .filters import PostFilter

class PostList(ListView): # общий класс отображения на странице всех новостей и статей
    model = Post
    ordering = '-time_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

class NewsList(PostList):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(news_post='NW')
class NewsPostList(PostList):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(news_post='PT')

class PostDetail(DetailView): #общий класс детальной страницы и для новости и для статьи
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    # def get_object(self, *args, **kwargs):
    #     obj = cache.get(f'post-{self.kwargs["pk"]}',
    #                     None)  # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.
    #     if not obj:
    #         obj = super().get_object(queryset=self.queryset)
    #         cache.set(f'post-{self.kwargs["pk"]}', obj)
    #     return obj
class NewsPostDetail(PostDetail):

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(news_post='NW')

class PostPostDetail(PostDetail):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(news_post='PT')


class SearchList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров

        return self.filterset.qs
    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset

        return context


class NewsCreate(PermissionRequiredMixin,CreateView):
    permission_required = ('news.add_post',)
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'
    success_url = reverse_lazy('post_list')

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super(NewsCreate, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        initial['author'] = self.request.user.pk
        return initial

    def form_valid(self, form):

        self.objects= form.save(commit=False)
        self.objects.news_post = 'NW'
        self.objects.author = Author.objects.get(pk= self.request.user.id)
        cat_id = self.request.POST.get('category')
        send_email_task.delay(cat_id)
        return super().form_valid(form)


class PostCreate(PermissionRequiredMixin,CreateView):
    permission_required = ('news.add_post',)
    form_class = NewsForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        news= form.save(commit=False)
        news.news_post = 'PT'
        return super().form_valid(form)

class PostUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = ('news.change_post',)

    form_class = NewsForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post_list')

class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

class Category_list_view(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'category_list'

def subscribe_me(request):
    if request.method =='POST':
        user = request.user
        form = CatForms()
        cat_id = request.POST.get('category')
        category = Category.objects.get(id=cat_id)
        category.subscribers.add(user)
        send_mail(
            subject = f'{user.username} вы подписались на категорию -{category}',
            message = 'спасибо что подписались',
            from_email = 'stoliktimofeev@gmail.com',
            recipient_list = [user.email],

        )

    else:
        form = CatForms()
    return render(request,'category_list.html',{'form':form})







