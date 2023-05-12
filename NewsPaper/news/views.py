# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail

from django.shortcuts import redirect, render
from .signals import postlimit, limit_post_signal

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,FormView

from .forms import NewsForm, CatForms
from .models import Post, Category
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


class NewsCreate(PermissionRequiredMixin,CreateView):
    permission_required = ('news.add_post',)
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        news= form.save(commit=False)
        news.news_post = 'NW'
        return super().form_valid(form)

    def post(self,request, *args, **kwargs):
        cat_id = request.POST.get('category')
        category = Category.objects.get(id=cat_id)
        list_= list(category.subscribers.values('email'))
        emaillist = []
        for i in list_:
            emaillist.append(i['email'])
        send_mail(
            subject=f' новая новость в категории -{category}',
            message='спасибо что подписались',
            from_email='stoliktimofeev@ya.ru',
            recipient_list=emaillist,
        )
        return super().post(request, *args, **kwargs)


    

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
            from_email = 'stoliktimofeev@ya.ru',
            recipient_list = [user.email],

        )

    else:
        form = CatForms()
    return render(request,'category_list.html',{'form':form})







