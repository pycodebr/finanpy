from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    """
    Configuration for the profiles app.

    Registers signal handlers when the app is ready to ensure
    automatic Profile creation when Users are created.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'

    def ready(self):
        """
        Import signal handlers when the app is ready.

        This method is called once Django has loaded all models and is ready
        to process signals. Importing signals here ensures they are registered
        and active when the application runs.
        """
        import profiles.signals  # noqa: F401
