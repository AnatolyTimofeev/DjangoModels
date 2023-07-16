import datetime
from datetime import timedelta
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.dispatch import Signal
from django.core.mail import mail_managers
from .models import Post
limit_post_signal=Signal()

@receiver(pre_save,sender=Post)
def postlimit(sender,instance,**kwargs):

   author = instance.author.user.id
   delta =timedelta(days=1)
   posts = Post.objects.filter(author=author,time_in__range=(datetime.datetime.now()-delta, datetime.datetime.now())).count()
   if posts >3:
      raise Exception('Вы не можете отправлять больше трех новостей в сутки')
















