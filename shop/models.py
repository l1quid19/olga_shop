from django.db import models
from django.contrib.auth.models import User

# 1. Категории товаров
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(unique=True, verbose_name="URL-имя")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

# 2. Товары
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Категория")
    name = models.CharField(max_length=200, verbose_name="Название товара")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    unit = models.CharField(max_length=20, default='шт', verbose_name="Единица измерения (шт, кг)")
    stock = models.PositiveIntegerField(default=0, verbose_name="Остаток на складе")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Фото товара")
    is_available = models.BooleanField(default=True, verbose_name="Доступен для заказа")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

# 3. Заказы
class Order(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создан'),
        ('confirmed', 'Подтверждён'),
        ('ready', 'Готов к выдаче'),
        ('completed', 'Завершён'),
        ('cancelled', 'Отменён'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Клиент")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.CharField(max_length=250, verbose_name="Адрес доставки (или Самовывоз)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f"Заказ №{self.id} от {self.user.username}"

    # Метод для вычисления итоговой суммы заказа
    @property
    def total_price(self):
        return sum(item.price * item.quantity for item in self.items.all())

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

# 4. Позиции в заказе (Корзина)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена на момент заказа")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

# 5. История статусов заказа
class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Order, related_name='status_history', on_delete=models.CASCADE, verbose_name="Заказ")
    old_status = models.CharField(max_length=20, verbose_name="Старый статус")
    new_status = models.CharField(max_length=20, verbose_name="Новый статус")
    changed_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата изменения")
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Кто изменил")

    class Meta:
        verbose_name = "История статусов"
        verbose_name_plural = "История статусов"

        # 6. Попытки входа (для защиты от Brute Force)
class LoginAttempt(models.Model):
    username = models.CharField(max_length=150, verbose_name="Логин")
    ip_address = models.GenericIPAddressField(verbose_name="IP-адрес")
    is_success = models.BooleanField(default=False, verbose_name="Успешно")
    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name="Время попытки")

    class Meta:
        verbose_name = "Попытка входа"
        verbose_name_plural = "Попытки входа"