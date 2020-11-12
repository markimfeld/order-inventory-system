from django.contrib.auth import authenticate, login as do_login, logout as do_logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse

from .forms import LoginForm

# Create your views here.

def login(request):
    if not request.user.is_authenticated:
        form = LoginForm()

        if request.method == 'POST':
            form = LoginForm(data=request.POST)

            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                user = authenticate(request, username=username, password=password)
                

                if user is not None:
                    do_login(request, user)
                    return HttpResponseRedirect(reverse('core:index'))
        return render(request, 'users/login.html', {'form': form})
    else:
        return HttpResponseRedirect(reverse('core:index'))

def logout(request):
    if request.user.is_authenticated:
        do_logout(request)
        return HttpResponseRedirect(reverse('users:login'))
