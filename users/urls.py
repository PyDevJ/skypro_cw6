from django.urls import path
from django.views.decorators.cache import cache_page

from users.views import RegisterView, CodeView, LoginView, UserUpdate, UserTemplateView, new_password, \
    PasswordsChangeView
from users.apps import UsersConfig
from . import views

app_name = UsersConfig.name

urlpatterns = [
    path('', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.LogoutUser, name='logout'),
    path('code/', CodeView.as_view(), name='code'),
    path('profile/', UserUpdate.as_view(), name='profile'),
    # path('template/', cache_page(60)(UserTemplateView.as_view()), name='template'),
    path('template/', UserTemplateView.as_view(), name='template'),
    path('template/newpassword', new_password, name='new_password'),
    path('user_password/', PasswordsChangeView.as_view(), name='user_password'),
]
