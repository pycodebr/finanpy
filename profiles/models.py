from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Profile(models.Model):
    """
    Model representing a user profile with additional information.

    Automatically created via signal when a User is created.
    Contains personal information not included in Django's User model.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Usuário'
    )
    full_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Nome Completo'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Telefone'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
        ordering = ['-created_at']

    def __str__(self):
        """Return full_name if exists, otherwise return user email."""
        if self.full_name:
            return self.full_name
        return self.user.email if hasattr(self.user, 'email') else self.user.username
