from django.urls import path
from .views import news_list, news_detail, home, contact, notFoundPage

urlpatterns = [
    path('', home, name='home_page'),
    path('contact', contact, name='contact_page'),
    path('not-found/', notFoundPage, name='not-found'),
    path('news/', news_list, name='news_list'),
    path('news/<int:id>/', news_detail, name='news_detail'),
]
