from django.urls import path
# Импортируем созданные нами представления
from .views import PostList, PostDetail, SearchList, NewsCreate, PostCreate, PostUpdate, PostDelete

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostList.as_view(), name = 'post_list'),

   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', PostDetail.as_view()),
   path('search/', SearchList.as_view()),
   path('news/create/', NewsCreate.as_view()),
   path('articles/create/', PostCreate.as_view()),
   path('articles/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('news/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('articles/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
]