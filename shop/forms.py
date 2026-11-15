from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from .models import LoginAttempt
from django.utils import timezone
from datetime import timedelta

# Форма входа с защитой от Brute Force
class SecureLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        
        ip = self.request.META.get('REMOTE_ADDR')
        time_threshold = timezone.now() - timedelta(minutes=15)
        failed_attempts = LoginAttempt.objects.filter(
            username=user.username,
            ip_address=ip,
            is_success=False,
            attempt_time__gte=time_threshold
        ).count()
        
        if failed_attempts >= 5:
            raise ValidationError(
                "Слишком много неудачных попыток входа. Ваш аккаунт временно заблокирован на 15 минут.",
                code='too_many_attempts',
            )

# Новая форма регистрации с галочкой согласия
class CustomUserCreationForm(UserCreationForm):
    agree_to_terms = forms.BooleanField(
        required=True,
        label="Я согласен на обработку персональных данных",
        error_messages={'required': 'Вы должны согласиться с политикой обработки данных.'}
    )

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields