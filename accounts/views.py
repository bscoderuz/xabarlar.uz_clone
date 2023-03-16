from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views import View

from .models import Profile
from .forms import LoginForm, UserRegisterForm, UserEditForm, ProfileEditForm
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
            Profile.objects.create(user=new_user)
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


@login_required
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

@login_required
def dashboard(request):
    user = request.user
    profile_info = Profile.objects.get(user=user)
    context = {
        'user': user,
        'profile_info': profile_info
    }
    return render(request, 'pages/user-profile.html', context)

@login_required
def edit_user(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'account/profile_edit.html', context)


class EditUserView(View):

    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'account/profile_edit.html', context)

    def post(self, request):
        if request.method == "POST":
            user_form = UserEditForm(instance=request.user,
                                     data=request.POST)
            profile_form = ProfileEditForm(instance=request.user.profile,
                                           data=request.POST,
                                           files=request.FILES)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                return redirect('profile')
