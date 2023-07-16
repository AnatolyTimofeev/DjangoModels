import datetime
from celery import shared_task
import time

from django.core.mail import send_mail

from news.models import Category, Post

@shared_task
def send_email_task(id):  # посылаем письмо подписчикам категории сразу после добавления новости
    category = Category.objects.get(id=id)
    if category.subscribers.count() > 0:
        list_ = list(category.subscribers.values('email'))
        emaillist = []
        for i in list_:
            emaillist.append(i['email'])
        send_mail(
            subject=f' новая новость в категории -{category}',
            message='спасибо что подписались',
            from_email='stoliktimofeev@gmail.com',
            recipient_list=emaillist,
        )


@shared_task
def my_job(): # раз в неделю посылается список новостей за последние 7 дней полписчикам категории
    category = Category.objects.all()
    delta = datetime.timedelta(days=7)

    for cat in category:
        posts = Post.objects.filter(category=cat,time_in__range=(datetime.datetime.now() - delta, datetime.datetime.now()))
        list_= list(cat.subscribers.values('email'))
        emaillist =[]
        for i in list_:
            emaillist.append(i['email'])
        if cat.subscribers.all().count() > 0 and posts.count() > 0:
            send_mail(
                subject=f'список статей в категории{cat}',
                message= f'посмотрите статьи за последние 7 дней{posts}',
                from_email = 'stoliktimofeev@gmail.com',
                recipient_list = emaillist,
            )
