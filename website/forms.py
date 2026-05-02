from django import forms
from django.contrib.auth.models import User
from . import models


class RegistrationForm(forms.Form):
    nickname = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nickname'
        })
    )
    password = forms.CharField(
        min_length=8,
        max_length=50,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'})
    )
    confirm_password = forms.CharField(
        min_length=8,
        max_length=50,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    })
    )

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        if User.objects.filter(username=nickname).exists():
            raise forms.ValidationError('User with this nickname already exists')
        return nickname

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('User with this email already exists')
        return email


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = ['avatar', 'bio', 'birth_date']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Bio'}),
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')

        if avatar:
            if avatar.size > 2 * 1024 * 1024:
                raise forms.ValidationError('Avatar size is too big')

        return avatar


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        min_length=8,
        max_length=50,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Old Password'})
    )
    new_password = forms.CharField(
        min_length=8,
        max_length=50,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'New Password'})
    )
    new_password_confirmation = forms.CharField(
        min_length=8,
        max_length=50,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new Password'})
    )

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password = cleaned_data.get('new_password')
        new_password_confirmation = cleaned_data.get('new_password_confirmation')

        if new_password and new_password_confirmation:
            if new_password != new_password_confirmation:
                raise forms.ValidationError('Passwords do not match')

        if old_password and new_password:
            if old_password == new_password:
                raise forms.ValidationError('New password cannot be the same as old password')

        return cleaned_data

