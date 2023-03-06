from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy

from .forms import LoginForm, UserRegisterForm
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView


# Create your views here.

# class base view
class UserRegister(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'account/register.html'


# function base view
def user_register(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            context = {
                'new_user': new_user
            }
            return render(request, 'account/register_done.html', context)
    else:
        user_form = UserRegisterForm(request.POST)
        context = {
            'form': user_form
        }
    return render(request, 'account/register.html', context)


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request,
                username=data['username'],
                password=data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Muvaffaqiyatli login amalga oshirildi!")
                else:
                    return HttpResponse("Sizning profilingiz faol emas")

            else:
                return HttpResponse("Login va parolda xatolik bor!")
    else:
        form = LoginForm()
        context = {
            'form': form,
        }
    return render(request, 'registration/login.html', context)


def dashboard(request):
    user = request.user

    context = {
        'user': user
    }
    return render(request, 'pages/user-profile.html', context)


def user_profile(request):
    pass
