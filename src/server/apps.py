from django.apps import AppConfig


class Server(AppConfig):
    name = 'server'
    verbose_name = "Market Graph"

    def ready(self):
        pass
