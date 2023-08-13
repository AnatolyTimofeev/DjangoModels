from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from newsportal.views import UserRegisterView, verify_code, UserProfileView, UserLoginView, PostCreateView, \
    PostListView, ReplyCreateView, delete_reply, accept_reply

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('otp/',verify_code, name='verify_code'),
    path('accounts/login/', UserLoginView.as_view(), name='login'),
    path('accounts/profile/<int:pk>/', UserProfileView.as_view(), name='user_profile'),
    path('accounts/logout/', LogoutView.as_view(), name= 'logout'),
    path('create/', PostCreateView.as_view(), name='create_post'),
    path('posts/', PostListView.as_view(), name='posts'),
    path('reply/create/<int:post_id>/', ReplyCreateView.as_view(), name='create_reply'),
    path('delete_reply/<int:pk>/', delete_reply, name='delete_reply'),
    path('accept_reply/<int:pk>/', accept_reply, name='accept_reply'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)