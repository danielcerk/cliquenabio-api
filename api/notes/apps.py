from django.apps import AppConfig


class NotesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.notes'

    def ready(self):
        
        import api.notes.signals
