from django.contrib import admin
from django.urls import path, include
from shop import views
from shop.forms import SecureLoginForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    
    # Наша защищенная страница входа
    path('accounts/login/', views.SecureLoginView.as_view(), name='login'),
    
    # Остальные стандартные пути (выход и т.д.)
    path('accounts/', include('django.contrib.auth.urls')), 
    
    # Наши пути для магазина
    path('register/', views.register, name='register'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('profile/', views.profile, name='profile'),
    path('contacts/', views.contacts, name='contacts'),
]