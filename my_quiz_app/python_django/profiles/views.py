# profiles/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

@login_required
def profile(request):
    profile = request.user.userprofile
    return render(request, 'profiles/profile.html', {'profile': profile})

def search_user(request):
    query = request.GET.get('query')
    if query:
        results = UserProfile.objects.filter(Q(user__username__icontains=query) | Q(user__id__icontains=query))
    else:
        results = []
    return render(request, 'profiles/search.html', {'results': results})
