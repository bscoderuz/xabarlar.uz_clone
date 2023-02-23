from django.shortcuts import render

from news_app.models import News


# Create your views here.

def news_list(request):
    news = News.objects.all()

    context = {
        'news': news
    }
    return render(request, 'news/news_list.html', context)
