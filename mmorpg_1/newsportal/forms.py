from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.mail import send_mail

from newsportal.models import Post, Reply, EmailCampaign


class RegisterUserForm(UserCreationForm):
    username = forms.CharField()
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username','email')

class VerificationCodeForm(forms.Form):
    verification_code = forms.CharField(label='Одноразовый код', max_length=4)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content_text', 'photo', 'video','categories']
    # photo = forms.ImageField(required=False)
    # video = forms.FileField(required=False)

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'placeholder': 'Введите ваш отзыв'}),
        }


class ReplyFilterForm(forms.Form):
    # author = forms.ModelChoiceField(queryset=User.objects.none(), required=False)
    author = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].queryset = User.objects.filter(post__author=user).distinct()


class EmailCampaignForm(forms.ModelForm):
    class Meta:
        model = EmailCampaign
        fields = ['title', 'subject', 'message', 'recipients']

