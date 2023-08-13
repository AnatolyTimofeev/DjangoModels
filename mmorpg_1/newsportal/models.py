from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    verification_code = models.CharField(max_length=4, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username



class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content_text = models.TextField()
    photo = models.ImageField(upload_to='photos/')
    video = models.FileField(upload_to='videos/')
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, related_name='posts')

    def __str__(self):
        return self.title

class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='replies')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Response by {self.user.username} to '{self.post.title}'"

from django.db import models
from django.contrib.auth.models import User

class EmailCampaign(models.Model):
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    recipients = models.ManyToManyField(User, related_name='campaigns', blank=True)
    sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def send_emails(self):
        recipients_emails = self.recipients.values_list('email', flat=True)
        subject = self.subject
        message = self.message
        from_email = 'stoliktimofeev@gmail.com'

        send_mail(subject, message, from_email, recipients_emails)
        self.sent = True
        self.save()



