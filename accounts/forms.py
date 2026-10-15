"""МОДУЛЬ 1 (АВТОРИЗАЦИЯ): формы. Формы для входа и регистрации."""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class LoginForm(AuthenticationForm):
    """Форма входа. Стандартная, но с русскими подписями."""
    username = forms.CharField(
        label="Email или логин",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите email"})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Введите пароль"})
    )


class RegisterForm(UserCreationForm):
    """Форма регистрации нового сотрудника."""
    full_name = forms.CharField(label="ФИО", max_length=150)
    email = forms.EmailField(label="Email")
    phone = forms.CharField(label="Телефон", max_length=20, required=False)

    class Meta:
        model = User
        fields = ("username", "full_name", "email", "phone", "position")

    def save(self, commit=True):
        """Сохраняем full_name в first_name/last_name."""
        user = super().save(commit=False)
        parts = self.cleaned_data["full_name"].split(maxsplit=1)
        user.first_name = parts[0] if parts else ""
        user.last_name = parts[1] if len(parts) > 1 else ""
        if commit:
            user.save()
        return user
