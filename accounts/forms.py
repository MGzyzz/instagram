from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model

from accounts.models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control mb-3'})
    )

    password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control mb-3'
            }
        )
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:

            user_model = get_user_model()
            if '@' in username:
                user = user_model.objects.filter(email=username).first()
            else:
                user = user_model.objects.filter(username=username).first()

            if user is not None and user.check_password(password):
                self.user_cache = user
            else:
                self.add_error('username', 'Invalid login/email or password.')

        return self.cleaned_data


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
        })
    )

    avatar = forms.ImageField(
        label='Avatars',
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'placeholder': 'avatar',
        })
    )

    first_name = forms.CharField(
        label='Name',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name',
        }), required=False
    )

    user_information = forms.CharField(
        label='User Information',
        widget=forms.Textarea(attrs={
            'class': 'textarea-width',
            'placeholder': 'About me'
        }), required=False
    )

    phone_number = forms.CharField(
        label='Phone_number',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}
                               ), required=False
    )

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    gender = forms.ChoiceField(
        label='Gender',
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control mb-3'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'avatar', 'password1', 'password2', 'first_name', 'user_information',
                  'phone_number', 'gender']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']
