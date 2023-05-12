import datetime

from django.core.mail import send_mail

from NewsPaper.news.models import Category, Post


def my_job():
    category = Category.objects.all()
    delta = datetime.timedelta(days=7)

    for cat in category:
        posts = Post.objects.filter(category=cat,time_in__range=(datetime.datetime.now() - delta, datetime.datetime.now()))
        list_= list(cat.subscribers.values('email'))
        if cat.subscribers.all().count() > 0 and posts.count() > 0:
            send_mail(
                subject=f'список статей в категории{cat}',
                message= f'посмотрите статьи за последние 7 дней{posts}',
                from_email = 'stoliktimofeev@ya.ru',
                recipient_list = [list_],
            )
