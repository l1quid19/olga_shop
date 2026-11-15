from django.contrib import admin
from .models import Category, Product, Order, OrderItem, OrderStatusHistory, LoginAttempt

# Настройка отображения товаров
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name',)

# Настройка отображения категорий
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

# Позиции внутри заказа
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('price',)

# Настройка отображения заказов
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'phone', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('phone', 'first_name', 'user__username')
    inlines = [OrderItemInline]

# История статусов
@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('order', 'old_status', 'new_status', 'changed_at', 'changed_by')
    readonly_fields = ('order', 'old_status', 'new_status', 'changed_at', 'changed_by')

    def has_add_permission(self, request):
        return False

# Попытки входа (Brute Force)
@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ('username', 'ip_address', 'is_success', 'attempt_time')
    list_filter = ('is_success', 'attempt_time')
    search_fields = ('username', 'ip_address')