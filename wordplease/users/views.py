# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.shortcuts import render,redirect
from django.contrib.auth import logout as django_logout,authenticate, login as django_login
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from users.forms import LoginForm,UserCreateForm
from django.views.generic import View

class LoginView(View):

    @csrf_exempt
    def get(self,request):
        error_messages = []
        form = LoginForm()
        context = {
            'errors': error_messages,
            'form': form
        }
        return render(request, 'users/login.html',context)

    @csrf_exempt
    def post(self,request):

        error_messages = []
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('usr')
            password = form.cleaned_data.get('pwd')
            user = authenticate(username=username,password=password)
            if user is None:
                error_messages.append('Nombre Usuario o Contraseña incorrectos')
            else:
                if user.is_active:
                    django_login(request, user)
                    url= request.GET.get('next','home')
                    return redirect(url)
                else:
                    error_messages.append('El usuario no está activo')
        context = {
            'errors': error_messages,
            'form': form
        }
        return render(request, 'users/login.html',context)

def logout(request):
    if request.user.is_authenticated():
        django_logout(request)
    return redirect('home')

class SignupView(View):

    def get(self,request):
        form=UserCreateForm()
        context = {
            'form' : form
        }
        return render(request, 'users/new-user.html', context)


    def post(self,request):
       user = User()
       form=UserCreateForm(request.POST,instance=user)
       success_message = None
       if form.is_valid():
           new_post=form.save()
           success_message = 'Guardado con éxito'
           form = UserCreateForm()
       context = {
            'form' : form,
            'success_message' : success_message
       }
       return render(request, 'users/new-user.html',context)


