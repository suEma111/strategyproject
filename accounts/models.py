from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pass
    # 他のフィールド

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # related_name を設定
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # related_name を設定
        blank=True
    )