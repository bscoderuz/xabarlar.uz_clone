from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
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


def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {
        'news': news
    }
    return render(request, 'news/news_detail.html', context)


# function base view
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


# class base view
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


class LocalNewsView(ListView):
    model = News
    template_name = 'news/local-news.html'
    context_object_name = 'local_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Mahalliy")
        return news


class EuroNewsView(ListView):
    model = News
    template_name = 'news/euro-news.html'
    context_object_name = 'euro_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Xorij")
        return news


class TexnoNewsView(ListView):
    model = News
    template_name = 'news/texno-news.html'
    context_object_name = 'texno_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Texnologiya")
        return news


class SportNewsView(ListView):
    model = News
    template_name = 'news/sport-news.html'
    context_object_name = 'sport_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Sport")
        return news


class NewsUpdateView(UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'category', 'status',)
    template_name = 'crud/news-edit.html'


class NewsDeleteView(DeleteView):
    model = News
    template_name = 'crud/news-delete.html'
    success_url = reverse_lazy('home_page')


class NewsCreateView(CreateView):
    model = News
    template_name = 'crud/news-create.html'
    fields = ('title', 'slug', 'body', 'image', 'category', 'status',)
