from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from .models import Post, Category, PostCategory, Author
from django.core.exceptions import ValidationError


class NewsForm(forms.ModelForm):


    class Meta:
       model = Post
       fields = [
                 'title',
                 'text',
                 'category',
                 'author',


       ]

class CatForms(forms.ModelForm):
    class Meta:
        model = PostCategory
        fields =['category',]

   # def clean(self):
   #     cleaned_data = super().clean()
   #     description = cleaned_data.get("description")
   #     if description is not None and len(description) < 20:
   #         raise ValidationError({
   #             "description": "Описание не может быть менее 20 символов."
   #         })
   #     name = cleaned_data.get("name")
   #     if name == description:
   #         raise ValidationError(
   #             "Описание не должно быть идентично названию."
   #         )
   #
   #     return cleaned_data
