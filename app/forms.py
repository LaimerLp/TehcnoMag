# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import Comment  # Добавлено Comment
from .models import BlogPost, Product, Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'address', 'phone', 'email']
        labels = {
            'full_name': _('ФИО'),
            'address': _('Адрес'),
            'phone': _('Телефон'),
            'email': _('Email'),
        }

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'summary', 'content', 'image']
        labels = {
            'title': _('Заголовок'),
            'summary': _('Краткое содержание'),
            'content': _('Содержание'),
            'image': _('Изображение'),
        }
        help_texts = {
            'image': _('Файл не выбран'),
        }

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator, MinLengthValidator

class FeedbackForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=100)
    email = forms.EmailField(label='Email')
    rating = forms.ChoiceField(label='Оценка сайта', choices=[(i, str(i)) for i in range(1, 6)])
    comments = forms.CharField(label='Комментарии', widget=forms.Textarea)
    subscribe = forms.BooleanField(label='Подписаться на новости', required=False)
    suggestions = forms.CharField(label='Предложения', widget=forms.Textarea, required=False)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']
        labels = {
            'name': _('Название'),
            'description': _('Описание'),
            'price': _('Цена'),
            'image': _('Изображение'),
        }
