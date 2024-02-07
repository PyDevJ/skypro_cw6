from django.urls import path
from django.views.decorators.cache import cache_page

from . import views
from message.apps import MessageConfig
from .views import ContactView, HomeListView

app_name = MessageConfig.name
urlpatterns = [
    # path('', cache_page(60)(HomeListView.as_view()), name='home'),
    path('', HomeListView.as_view(), name='home'),
    # path('contact/', cache_page(60)(ContactView.as_view()), name='contact'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('client_create/', views.ClientCreateView.as_view(), name='client_create'),
    path('update/<int:pk>', views.ClientUpdateView.as_view(), name='update_client'),
    path('list/', views.ClientListView.as_view(), name='client_list'),
    path('delete/<int:pk>/detail/', views.ClientDeleteView.as_view(), name='delete'),
    path('mailings_list/', views.MailingsListView.as_view(), name='mailings_list'),
    path('mailings_create/', views.MailingsCreateView.as_view(), name='mailings_create'),
    path('update_mailings/<int:pk>/detail/', views.MailingsUpdateView.as_view(), name='update_mailings'),
    path('delete_mailings/<int:pk>/detail/', views.MailingsDeleteView.as_view(), name='delete_mailings'),
    path('Message_list/', views.MessageListView.as_view(), name='message_list'),
    path('message_create/', views.MessageCreateView.as_view(), name='message_create'),
    path('message_update/<int:pk>/detail/', views.MessageUpdateView.as_view(), name='message_update'),
    path('message_delete/<int:pk>/detail/', views.MessageDeleteView.as_view(), name='message_delete'),
]
