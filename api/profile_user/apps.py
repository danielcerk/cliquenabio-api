from django.apps import AppConfig


class ProfileUserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.profile_user'

    def ready(self):
        
        import api.profile_user.signals
