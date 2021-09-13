from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    # Import the signals declared in signals.py (this is just Django a Django convention intended to avoid side effects)
    def ready(self):
        import users.signals
