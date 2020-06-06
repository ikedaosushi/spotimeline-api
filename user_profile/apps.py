from django.apps import AppConfig
import signals

class ProfilesConfig(AppConfig):
    name = 'profiles'

    def ready(self):
        pass
