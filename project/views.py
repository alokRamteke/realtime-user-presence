from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from .models import Profile
from django.utils import timezone


User = get_user_model()


@login_required(login_url='/log_in/')
def user_list(request):
    """
    NOTE: This is fine for demonstration purposes, but this should be
    refactored before we deploy this app to production.
    Imagine how 100,000 users logging in and out of our app would affect
    the performance of this code!
    """
    users = User.objects.select_related('logged_in_user')
    for user in users:
        if hasattr(user, 'logged_in_user'):
            user.status = 'Online'
        elif Profile.objects.filter(user=user):
            last_activity = Profile.objects.filter(user=user)[0].last_activity
            inactive_time = timezone.now() - last_activity
            if inactive_time.total_seconds() > 15 and inactive_time.total_seconds() <= 300:
                user.status = 'Away'
            else:
                user.status = 'Offline'

    return render(request, 'user_list.html', {'users': users})


def log_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(reverse('project:user_list'))
        else:
            print(form.errors)
    return render(request, 'project/log_in.html', {'form': form})


@login_required(login_url='/log_in/')
def log_out(request):
    logout(request)
    return redirect(reverse('project:log_in'))


def sign_up(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('project:log_in'))
        else:
            print(form.errors)
    return render(request, 'project/sign_up.html', {'form': form})