from django.urls import path
from .views import IndexView
from django.views.decorators.cache import cache_page
urlpatterns = [
    path('', (IndexView.as_view())),
]