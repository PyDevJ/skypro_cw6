from users.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django import forms


class UserForm(UserCreationForm):
    password1 = forms.CharField(label='Пароль1', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пороля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    email = forms.CharField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    avatar = forms.ImageField(label='avatar', widget=forms.FileInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('email', 'avatar', 'password1', 'password2')


class PasswordChangingForm(PasswordChangeForm):
    pass


class UserFormUpdate(UserChangeForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-input'}))
    surname = forms.CharField(label='Отчество', widget=forms.TextInput(attrs={'class': 'form-input'}))
    avatar = forms.ImageField(label='avatar', widget=forms.FileInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'surname', 'avatar')

    def __init__(self, *args, **kwargs):
        super(UserFormUpdate, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
