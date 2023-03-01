from django.urls import path
from .views import news_list, news_detail, home, contact, notFoundPage, HomePageView, LocalNewsView, EuroNewsView, \
    TexnoNewsView, SportNewsView, NewsUpdateView, NewsDeleteView, NewsCreateView

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('news/', news_list, name='news_list'),
    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('news/<slug:news>/', news_detail, name='news_detail'),
    path('news/<slug>/edit/', NewsUpdateView.as_view(), name='news_edit'),
    path('news/<slug>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('local-news/', LocalNewsView.as_view(), name='local-news'),
    path('euro-news/', EuroNewsView.as_view(), name='euro-news'),
    path('sport-news/', SportNewsView.as_view(), name='sport-news'),
    path('texno-news/', TexnoNewsView.as_view(), name='texno-news'),
    path('not-found/', notFoundPage, name='not_found'),
    path('contact/', contact, name='contact_page'),

]
