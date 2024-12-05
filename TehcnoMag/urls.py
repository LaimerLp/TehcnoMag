# urls.py
from datetime import datetime
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('links/', views.links, name='links'),
    path('pool/', views.pool, name='pool'),
    path('thank_you/', views.thank_you, name='thank_you'),
    path('register/', views.registration, name='register'),
    path('admin/', admin.site.urls),
    path('blog/', views.blog_list, name='blog_list'),
    path('post/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('add_blog_post/', views.add_blog_post, name='add_blog_post'),
    path('login/',
     LoginView.as_view(
         template_name='app/login.html',
         authentication_form=forms.BootstrapAuthenticationForm,
         extra_context={
             'title': 'Авторизация',
             'year': datetime.now().year,
         },
         redirect_authenticated_user=True,
         next_page='home'  # Перенаправление на главную страницу после входа
     ),
     name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('advantages/', views.advantages, name='advantages'),
    path('video/', views.video, name='video'),  # Новый URL-шаблон для страницы "Видео"
    path('accounts/login/',
     LoginView.as_view(
         template_name='app/login.html',
         authentication_form=forms.BootstrapAuthenticationForm,
         extra_context={
             'title': 'Авторизация',
             'year': datetime.now().year,
         }
     ),
     name='accounts_login'),  # Добавлен URL-шаблон для accounts/login/
    path('ckeditor/', include('ckeditor_uploader.urls')),  # Добавьте эту строку
    path('products/', views.products, name='products'),  # Новый URL-шаблон для страницы "Товары"
    path('product/<int:pk>/', views.product_detail, name='product_detail'),  # Новый URL-шаблон для отображения отдельного товара
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # Новый URL-шаблон для добавления товаров в корзину
    path('cart/', views.cart, name='cart'),  # Новый URL-шаблон для страницы "Корзина"
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),  # Новый URL-шаблон для удаления товаров из корзины
    path('checkout/', views.checkout, name='checkout'),  # Новый URL-шаблон для оформления заказа
    path('order_success/', views.order_success, name='order_success'),  # Новый URL-шаблон для страницы успешного оформления заказа
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
