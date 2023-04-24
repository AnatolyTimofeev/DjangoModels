# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import NewsForm
from .models import Post
from .filters import PostFilter


class PostList(ListView):

    model = Post
    ordering = '-time_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 2


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'

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


class NewsCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        news= form.save(commit=False)
        news.news_post = 'NW'
        return super().form_valid(form)
class PostCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        news= form.save(commit=False)
        news.news_post = 'PT'
        return super().form_valid(form)

class PostUpdate(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post_list')

class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
