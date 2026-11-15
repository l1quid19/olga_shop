from django.contrib import admin
from django.urls import path, include, re_path
from shop import views
from shop.forms import SecureLoginForm

# Импорты для раздачи медиафайлов
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

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
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('profile/', views.profile, name='profile'),
    path('contacts/', views.contacts, name='contacts'),
]

# Раздача медиафайлов (картинок товаров)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]