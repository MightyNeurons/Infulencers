from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'App'

    #def ready(self):
        #from App import views
        #views.Update_Start()
