from django.urls import path, include
# Импортируем созданные нами представления
from .views import PostList, PostDetail, SearchList, NewsCreate, PostCreate, PostUpdate, PostDelete, subscribe_me, \
   NewsList, NewsPostList, NewsPostDetail, PostPostDetail
from django.views.decorators.cache import cache_page

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostList.as_view(),name='post_list'),

   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('news/<int:pk>', NewsPostDetail.as_view()),
   path('articles/<int:pk>', PostPostDetail.as_view()),
   path('search/', SearchList.as_view()),
   path('news/create/', NewsCreate.as_view()),
   path('articles/create/', PostCreate.as_view()),
   path('articles/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('news/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('articles/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('categories/', subscribe_me, name = 'categories'),
   # path('subscribe/', subscribe_me, name = 'subscribe'),
   path('news/', NewsList.as_view()),
   path('articles/', NewsPostList.as_view()),

]