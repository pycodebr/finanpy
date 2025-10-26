from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Profile(models.Model):
    '''
    User profile model containing additional personal information.

    This model is automatically created via post_save signal when a User is
    created (see profiles/signals.py). It extends the core User model with
    optional personal details like full name and phone number.

    Attributes:
        user: One-to-one relationship with CustomUser (CASCADE on delete)
        full_name: Optional full name of the user
        phone: Optional phone number
        created_at: Timestamp when profile was created (auto-generated)
        updated_at: Timestamp when profile was last modified (auto-updated)

    Relationships:
        - One-to-one with CustomUser via user field
        - Related name: user.profile

    Example:
        profile = request.user.profile
        profile.full_name = 'João Silva'
        profile.save()
    '''
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
        indexes = [
            models.Index(fields=['user']),
        ]

    def __str__(self):
        '''
        Return string representation of the profile.

        Returns full_name if provided, otherwise falls back to user's email.
        This ensures a meaningful display in admin and template contexts.

        Returns:
            str: Full name if available, otherwise user email
        '''
        if self.full_name:
            return self.full_name
        return self.user.email if hasattr(self.user, 'email') else self.user.username
