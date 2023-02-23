from django.urls import path
from .views import news_list

urlpatterns = [
    path('all/', news_list, name='news_list')
]
