from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import LoginAttempt
from django.utils import timezone
from datetime import timedelta

class SecureLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        
        # Считаем IP-адрес пользователя
        ip = self.request.META.get('REMOTE_ADDR')
        
        # Смотрим, сколько было неудачных попыток за последние 15 минут
        time_threshold = timezone.now() - timedelta(minutes=15)
        failed_attempts = LoginAttempt.objects.filter(
            username=user.username,
            ip_address=ip,
            is_success=False,
            attempt_time__gte=time_threshold
        ).count()
        
        # Если больше 5 — блокируем
        if failed_attempts >= 5:
            raise ValidationError(
                "Слишком много неудачных попыток входа. Ваш аккаунт временно заблокирован на 15 минут.",
                code='too_many_attempts',
            )