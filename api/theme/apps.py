from django.apps import AppConfig


class ThemeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.theme'

    def ready(self):

        import api.theme.signals
