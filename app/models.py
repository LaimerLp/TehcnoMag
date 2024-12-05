# models.py
from django.db import models
from django.contrib.auth.models import User
#from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='product_images/', null=True, blank=True, verbose_name="Изображение")
    quantity_in_basket = models.IntegerField(default=0, verbose_name="Количество товаров в корзине")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

class Feedback(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    rating = models.IntegerField(verbose_name="Оценка сайта", default=0)
    comments = models.TextField(verbose_name="Комментарии")
    subscribe = models.BooleanField(default=False, verbose_name="Подписаться на новости")
    suggestions = models.TextField(blank=True, null=True, verbose_name="Предложения")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Обратная связь"
        verbose_name_plural = "Обратная связь"

class BlogPost(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200)
    summary = models.TextField()
    content = RichTextUploadingField()  # Используйте RichTextField, если не нужна загрузка изображений
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 400 or img.width > 400:
                output_size = (400, 400)
                img.thumbnail(output_size)
                img.save(self.image.path)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.date}'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, verbose_name="ФИО")
    address = models.TextField(verbose_name="Адрес")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Order by {self.user.username} on {self.created_at}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"