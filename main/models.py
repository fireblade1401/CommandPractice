from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class MainSlider(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Добавить текст'
        verbose_name_plural = 'Текст на слайдер'


class Categories(models.Model):
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    product_image = models.ImageField(upload_to='products/')
    product_name = models.CharField(max_length=255)
    product_count = models.PositiveIntegerField()
    product_price = models.DecimalField(max_digits=14, decimal_places=2)

    def __str__(self):
        return f"{self.category}, {self.product_price}"

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.product.product_price * self.quantity

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f"{self.cart.user}, {self.product}, {self.quantity}"


class links(models.Model):
    facebook = models.TextField()
    twitter = models.TextField()
    linkedin = models.TextField()
    instagram = models.TextField()
    youtube = models.TextField()

    def __str__(self):
        return self.instagram

    class Meta:
        verbose_name = 'Ссылку'
        verbose_name_plural = 'Ссылки'


class Callback(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return f"{self.name}, {self.phone}"

    class Meta:
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'



