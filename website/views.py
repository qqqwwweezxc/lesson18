from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.models import User
from .models import UserProfile
from . import forms


def index(request: HttpRequest) -> HttpResponse:
    """Renders the index page."""
    return render(request, 'website/index.html')


def register_view(request: HttpRequest) -> HttpResponse:
    """Renders the register page."""
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['nickname'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )

            UserProfile.objects.create(user=user)

            login(request, user)
            return redirect('profile')
    else:
        form = forms.RegistrationForm()

    return render(request, 'website/registration_form.html', {'form': form})


@login_required
def edit_profile_view(request: HttpRequest) -> HttpResponse:
    """Renders the edit profile page."""
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = forms.UserProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        form = forms.UserProfileForm(instance=profile)

    return render(request, 'website/edit_profile.html', {
        'form': form
    })

@login_required
def change_password_view(request: HttpRequest) -> HttpResponse:
    """Renders the change password page."""
    if request.method == 'POST':
        form = forms.PasswordChangeForm(request.POST)
        if form.is_valid():
            old_pass = form.cleaned_data['old_password']
            new_pass = form.cleaned_data['new_password']

            if not request.user.check_password(old_pass):
                form.add_error('old_password', 'Wrong old password')
            else:
                request.user.set_password(new_pass)
                request.user.save()
                update_session_auth_hash(request, request.user)
                return redirect('profile')
    else:
        form = forms.PasswordChangeForm()

    return render(request, 'website/change_password.html', {'form': form})


@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    """Renders the profile page."""
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    return render(request, 'website/profile.html', {
        'profile': profile
    })