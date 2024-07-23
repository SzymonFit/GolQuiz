# my_quiz_app/python_django/users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import views as auth_views


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'account/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'account/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def password_reset(request):
    return auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html')(request)

def password_reset_done(request):
    return auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html')(request)

def password_reset_confirm(request, uidb64=None, token=None):
    return auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html')(request, uidb64=uidb64, token=token)

def password_reset_complete(request):
    return auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html')(request)
