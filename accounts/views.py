from django.contrib import messages, auth
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from .models import Users

# Create your views here.


def register(request):
    if request.POST:
        data = request.POST

        try:
            new_user = Users(first_name=data['first_name'], last_name=data['last_name'], email=data['email'])
            new_user.set_password(data['password'])
            new_user.save()

            messages.success(request, 'Registration Successful')
            return HttpResponseRedirect(reverse('auth:login'))
        except IntegrityError:
            messages.error(request, 'User with this email already exists')
            return HttpResponseRedirect(reverse('auth:register'))
    return render(request, 'accounts/register.html')


def login(request):
    if request.POST:
        data = request.POST

        # saving the page the user needs login access to
        request.session['next'] = request.GET.get('next')

        # verifying user has an account
        if Users.objects.filter(email=data['email']).count() == 0:
            messages.error(request, 'Email doesn\'t exist in our database')
            return HttpResponseRedirect(reverse('auth:login'))

        # authenticating user
        user = auth.authenticate(email=data['email'], password=data['password'])
        if user is not None:
            auth.login(request, user)

            # redirecting user to previous page if there is
            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET.get('next'))
            elif request.session.get('next'):
                return HttpResponseRedirect(request.session.get('next'))

            return HttpResponseRedirect(reverse('main:home'))

        messages.error(request, 'Incorrect password')
        return HttpResponseRedirect(reverse('auth:login'))
    return render(request, 'accounts/login.html')


def sign_out(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('auth:login'))
