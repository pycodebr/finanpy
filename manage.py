#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from decouple import config


def main():
    """Run administrative tasks."""
    # Check for environment-specific settings
    # First try to get from environment variable, then from .env file
    env = os.environ.get('DJANGO_ENV', config('DJANGO_ENV', default='development'))
    
    if env == 'production':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.production')
    elif env == 'development':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')
    else:
        # Default to development settings if environment is not specified or unknown
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
