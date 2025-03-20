from django.db import models
from django.contrib.auth.models import AbstractUser
import random

class User(AbstractUser):
    is_active = models.BooleanField(default=False)  # Пользователь неактивен по умолчанию

    # Указываем уникальные related_name для groups и user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="custom_user_set",  # Уникальное имя для обратной ссылки
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_set",  # Уникальное имя для обратной ссылки
        related_query_name="user",
    )

class ConfirmationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='confirmation_code')
    code = models.CharField(max_length=6)

    @staticmethod
    def generate_code():
        return ''.join(random.choices('0123456789', k=6))

    def __str__(self):
        return f"{self.user.username} - {self.code}"