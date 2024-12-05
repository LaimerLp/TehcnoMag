# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import FeedbackForm, CommentForm, BlogPostForm, OrderForm
from .models import Feedback, BlogPost, Comment, Product, CartItem, Order
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title': 'Главная страница',
            'year': datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title': 'Контакты',
            'message': 'Ваша страница контактов.',
            'year': datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title': 'О нас',
            'message': 'Страница описания вашего приложения.',
            'year': datetime.now().year,
        }
    )

def links(request):
    """Renders the links page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title': 'Полезные ресурсы',
            'year': datetime.now().year,
        }
    )

def pool(request):
    """Renders the pool page."""
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Сохраняем данные формы в сессию
            request.session['submitted_data'] = form.cleaned_data
            return redirect('thank_you')
    else:
        form = FeedbackForm()

    return render(
        request,
        'app/pool.html',
        {
            'title': 'Обратная связь',
            'message': 'Оставьте ваш отзыв',
            'form': form,
        }
    )

def thank_you(request):
    """Renders the thank you page."""
    submitted_data = request.session.get('submitted_data', {})
    return render(
        request,
        'app/thank_you.html',
        {
            'title': 'Спасибо за отзыв',
            'submitted_data': submitted_data,
            'year': datetime.now().year,
        }
    )

def registration(request):
    """Renders the registration page."""
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False
            reg_f.is_active = True
            reg_f.is_superuser = False
            reg_f.date_joined = datetime.now()
            reg_f.last_login = datetime.now()
            reg_f.save()
            login(request, reg_f)
            return redirect('home')
    else:
        regform = UserCreationForm()

    return render(
        request,
        'app/registration.html',
        {
            'regform': regform,
            'year': datetime.now().year,
        }
    )

def blog_list(request):
    posts = BlogPost.objects.all().order_by('-published_date')
    return render(request, 'app/blog.html', {'posts': posts})

@login_required
def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    comments = post.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog_detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'app/blog_detail.html', {'post': post, 'comments': comments, 'form': form})

def advantages(request):
    """Renders the advantages page."""
    return render(
        request,
        'app/advantages.html',
        {
            'title': 'Преимущества',
            'year': datetime.now().year,
        }
    )

@login_required
@user_passes_test(lambda u: u.is_staff)
def add_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog_list')
    else:
        form = BlogPostForm()
    return render(request, 'app/add_blog_post.html', {'form': form})

def video(request):
    return render(request, 'app/video.html', {
        'title': 'Видео',
    })

def products(request):
    products = Product.objects.all()
    return render(request, 'app/products.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'app/product_detail.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'app/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            # Очистка корзины после оформления заказа
            cart_items.delete()
            return redirect('order_success')
    else:
        form = OrderForm()

    return render(request, 'app/checkout.html', {'form': form, 'cart_items': cart_items, 'total_price': total_price})

def order_success(request):
    return render(request, 'app/order_success.html')
