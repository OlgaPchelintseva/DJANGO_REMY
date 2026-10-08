from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MealPlan
from datetime import date


class RegisterForm(UserCreationForm):
    error_messages = {
            'password_mismatch': 'Пароли не совпадают',
        }

    email = forms.EmailField(
        required = True,
        widget = forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Введите email'
        }),
        label = 'Электронная почта'
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
                self.fields[field_name].help_text = ''

        self.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Введите имя пользователя'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Введите пароль'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Повторите пароль'
        })
        self.fields['username'].label = 'Имя пользователя'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Такой E-mail уже существует!')
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')

        if not password:
            return password

        if len(password) < 8:
            raise forms.ValidationError('Пароль должен содержать не менее 8 символов.')
        
        has_letter = any(c.isalpha() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)

        if not (has_letter and has_digit and has_special):
            raise forms.ValidationError('Пароль должен содержать буквы, цифры и специальные символы.')

        return password

class MealPlanForm(forms.ModelForm):
    class Meta:
        model = MealPlan
        fields = ['meal_date', 'meal_type']
        widgets = {
            'meal_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input'
            }),
            'meal_type': forms.Select(attrs={
                'class': 'form-input'
            }),
        }

class ShoppingListPeriodForm(forms.Form):
    start_date = forms.DateField(
        initial = date.today,
        widget = forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-input'
        }),
        label = 'Дата начала'
    )

    end_date = forms.DateField(
        widget = forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-input'
        }),
        label = 'Дата окончания'
    )

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')

        if start and end and start > end:
            raise forms.ValidationError('Дата начала не может быть позже даты окончания.')
        return cleaned_data