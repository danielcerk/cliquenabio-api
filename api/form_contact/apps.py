from django.apps import AppConfig


class FormContactConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.form_contact'

    def ready(self):
        
        import api.form_contact.signals
