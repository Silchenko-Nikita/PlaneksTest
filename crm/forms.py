from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm, ImageField

from crm.models import UserProfile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label='Email', required=True)
    first_name = forms.CharField(label='Имя', required=False)
    last_name = forms.CharField(label='Фамилия', required=False)
    birthday = forms.DateField(label='День рождения', required=False)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Такой email уже зарегестрирован')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')
        return password2


class EmailAuthenticationForm(AuthenticationForm):

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email is not None and password is not None:
            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None:
                no_user = False

                try:
                    user = User.objects.get(email=email)
                    self.user_cache = authenticate(self.request, username=user.email, password=password)
                    if self.user_cache is None:
                        no_user = True
                except ObjectDoesNotExist:
                    no_user = True

                if no_user:
                    raise forms.ValidationError(
                        "Неправильные email или пароль",
                        code='invalid_login',
                        params={'username': self.username_field.verbose_name},
                    )
            else:
                self.confirm_login_allowed(self.user_cache)

    class Meta:
        model = User
        fields = ('email', 'password')


class UserDataForm(ModelForm):
    # first_name = forms.CharField(label='Имя', required=False)
    # last_name = forms.CharField(label='Фамилия', required=False)
    birthday = forms.DateField(label='День рождения', required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class AvatarForm(ModelForm):

    class Meta:
        model = UserProfile
        fields = ('avatar',)
