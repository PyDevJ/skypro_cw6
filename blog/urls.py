from django.urls import path
from .views import BlogDetailView
from .apps import BlogConfig

app_name = BlogConfig.name

urlpatterns = [
    path('blog_details/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
]
