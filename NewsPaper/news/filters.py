import django.forms
import django_filters
from django.forms import widgets, SelectDateWidget
from django_filters import FilterSet
from .models import *
class PostFilter(FilterSet):
   class Meta:
       model = Post
       fields = {

           'title': ['icontains'],
           'author__user__username': ['icontains'],
           'time_in':['lt'],
           'category__category_name':['icontains'],

       }
       widgets = {'time_in': widgets.DateInput}
       # filter_overrides ={models.DateTimeField:{
       #     'filter_class': django_filters.DateTimeFilter,
       #     'extra': lambda f:{
       #         'widget': django.forms.SelectDateWidget,
       #     }
       #
       # }
       # }
