from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView

from news_app.models import News, Category, Contact
from .forms import ContactForm


# Create your views here.

def news_list(request):
    # news_list = News.objects.filter(status=News.Status.Published)
    news_list = News.published.all()
    context = {
        'news_list': news_list
    }
    return render(request, 'news/news_list.html', context)


def news_detail(request, id):
    news = get_object_or_404(News, id=id, status=News.Status.Published)
    context = {
        'news': news
    }
    return render(request, 'news/news_detail.html', context)


def home(request):
    categories = Category.objects.all()
    news_list = News.published.all().order_by('-publish_time')[:10]
    local_one = News.published.filter(category__name="Siyosat").order_by('-publish_time')[:1]
    local_news = News.published.all().filter(category__name="Siyosat").order_by('-publish_time')[1:6]
    context = {
        'news_list': news_list,
        'categories': categories,
        'local_one': local_one,
        'local_news': local_news,
    }
    return render(request, 'news/home.html', context)


class HomePageView(ListView):
    model = News
    template_name = 'news/home.html'
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.published.all().order_by('-publish_time')[:10]
        context['local_news'] = News.published.all().filter(category__name="Mahalliy").order_by('-publish_time')[:5]
        context['euro_news'] = News.published.all().filter(category__name="Xorij").order_by('-publish_time')[:5]
        context['techno_news'] = News.published.all().filter(category__name="Texnologiya").order_by('-publish_time')[:5]
        context['sport_news'] = News.published.all().filter(category__name="Sport").order_by('-publish_time')[:5]
        return context


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return HttpResponse("Xabar yo'natildi")
    context = {
        'form': form
    }
    return render(request, 'news/contact.html', context)


# Class base view

# class ContactForm(TemplateView):
#     template_name = 'news/contact.html'
#
#     def get(self, request, *args, **kwargs):
#         form = ContactForm()
#         context = {
#             'form': form
#         }
#         return render(request, 'news/contact.html', context)
#
#     def post(self, request, *args, **kwargs):
#         form = ContactForm(request.POST)
#         if request.method == "POST" and form.is_valid():
#             form.save()
#             return HttpResponse("Xabar jo'natildi")
#         context = {
#             "form": form
#         }
#         return render(request, 'news/contact.html', context)


def notFoundPage(request):
    return render(request, 'news/404.html')
