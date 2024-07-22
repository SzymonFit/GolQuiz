from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

def home(request):
    if request.user.is_authenticated:
        return redirect('menu')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('menu')
    else:
        form = AuthenticationForm() 

    return render(request, 'home/home.html', {'form': form})