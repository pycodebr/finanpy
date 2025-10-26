from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    '''
    Custom manager for CustomUser model that uses email as the unique identifier.

    Extends Django's default UserManager to support email-based authentication
    instead of username-based authentication.
    '''

    def create_user(self, email, password=None, **extra_fields):
        '''
        Create and save a regular user with the given email and password.

        Args:
            email (str): User's email address (required, used for authentication)
            password (str): User's password (optional for social auth scenarios)
            **extra_fields: Additional fields to set on the user model

        Returns:
            CustomUser: The created user instance

        Raises:
            ValueError: If email is not provided
        '''
        if not email:
            raise ValueError('O usuário precisa de um email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        '''
        Create and save a superuser with the given email and password.

        Automatically sets is_staff, is_superuser, and is_active to True.
        Used by Django management commands like createsuperuser.

        Args:
            email (str): Superuser's email address
            password (str): Superuser's password
            **extra_fields: Additional fields to set on the user model

        Returns:
            CustomUser: The created superuser instance

        Raises:
            ValueError: If is_staff or is_superuser is not True
        '''
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ter is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    '''
    Custom user model that uses email instead of username for authentication.

    This model extends Django's AbstractUser but removes the username field
    and makes email the primary authentication identifier. A Profile is
    automatically created for each user via post_save signal.

    Attributes:
        email: Unique email address used for authentication
        created_at: Timestamp when the user was created (auto-generated)
        updated_at: Timestamp when the user was last modified (auto-updated)

    Note:
        Username field is disabled (set to None)
        EMAIL authentication is required for login
    '''
    username = None  # Disable username field
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    # Configure email as the authentication field
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        '''Return the user's email address as string representation.'''
        return self.email
