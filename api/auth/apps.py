from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.auth'
    label = 'api_custom_auth'

    def ready(self):
        
        import api.auth.signals