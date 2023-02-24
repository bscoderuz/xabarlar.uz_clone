from django.urls import path
from .views import news_list, news_detail

urlpatterns = [
    path('all/', news_list, name='news_list'),
    path('<int:id>/', news_detail, name='news_detail'),
]
