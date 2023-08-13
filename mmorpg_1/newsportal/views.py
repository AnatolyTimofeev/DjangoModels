import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.sessions.models import Session

from django.contrib.auth.models import User
from django.core.mail import send_mail

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DetailView, ListView

from newsportal.forms import RegisterUserForm, VerificationCodeForm, PostForm, ReplyForm, ReplyFilterForm
from newsportal.models import Profile, Post, Category, Reply


class UserRegisterView(CreateView):
    model = User
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = '/otp/'

    def generate_verification_code(self):
        return ''.join(random.choices('0123456789', k=4))

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        verification_code = self.generate_verification_code()
        Profile.objects.create(user=user,verification_code=verification_code)
        self.request.session['user_id'] = user.id


        # Отправка кода на email
        subject = 'Ваш верификационный код'
        message = f'Ваш верификационный код: {verification_code}'
        from_email = 'stoliktimofeev@gmail.com'
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)

        return response

def verify_code(request):
    error_message = None

    if request.method == 'POST':
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            entered_code = request.POST['verification_code']
            user_id = request.session.get('user_id')
            user = User.objects.get(id=user_id)
            profiler = Profile.objects.get(user=user)

            if entered_code and user.profile.verification_code == entered_code:

                profiler.is_verified = True
                profiler.save()

                return redirect(f'/accounts/profile/{user_id}')  # Подставьте ваш URL для успешной верификации
            else:
                error_message = "Неверный код верификации. Пожалуйста, попробуйте снова."
    else:
        form = VerificationCodeForm()

    return render(request, 'otp.html', {'form': form, 'error_message': error_message})

class UserLoginView(LoginView):
    redirect_authenticated_user = True
    success_url = '/about/'



class UserProfileView(LoginRequiredMixin,DetailView):
    model = User
    template_name = 'user_profile.html'
    context_object_name = 'user'

    # def get_object(self):
    #     pk = self.kwargs['user_id']
    #     user = get_object_or_404(User, id=pk)
    #     return user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.object.id
        user = User.objects.get(pk=user_id)

        user_posts = Post.objects.filter(author= user)


        # Получаем все отклики, связанные с объявлениями пользователя
        user_replies = Reply.objects.filter(reply__in=user_posts)

        reply_filter_form = ReplyFilterForm(user=user, data=self.request.GET)
        reply_filter_form.fields['author'].queryset = User.objects.all()

        author = self.request.GET.get('author')
        date = self.request.GET.get('date')
        if author:
            user_replies = user_replies.filter(reply__author=author)

        if date:
            user_replies = user_replies.filter(created_at__date=date)

        context['user_replies'] = user_replies
        context['user_posts'] = user_posts
        context['reply_filter_form'] = reply_filter_form

        return context

@require_POST
def delete_reply(request, pk):
    user = request.user
    reply = get_object_or_404(Reply, id=pk, user=user)
    reply.delete()
    return redirect(f'/accounts/profile/{user.id}')

@require_POST
def accept_reply(request, pk):
    user = request.user
    reply = get_object_or_404(Reply, id=pk, reply__author=user)
    reply.is_accepted = True
    reply.save()
    # отправка письма

    subject = 'Ваш отклик был принят'
    message = f'отзыв: автор - {reply.user} -- {reply.text}'
    from_email = 'stoliktimofeev@gmail.com'
    recipient_list = [reply.user.email]
    send_mail(subject, message, from_email, recipient_list)

    return redirect(f'/accounts/profile/{user.id}')


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'
    success_url = reverse_lazy('posts')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']



class ReplyCreateView(LoginRequiredMixin, CreateView):
    model = Reply
    form_class = ReplyForm
    template_name = 'create_reply.html'
    success_url = reverse_lazy('posts')

    def form_valid(self, form):
        form.instance.user = self.request.user
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, pk=post_id)
        text = form.cleaned_data['text']

        form.instance.reply = post
        # отправка письма
        subject = 'На ваше обьявление поступил отклик'
        message = f'отзыв: автор - {form.instance.user} -- {text}'
        from_email = 'stoliktimofeev@gmail.com'
        recipient_list = [post.author.email]

        send_mail(subject, message, from_email, recipient_list)
        return super().form_valid(form)