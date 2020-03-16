from django.apps import AppConfig
from .decorators import only_run_on_server


class CasesConfig(AppConfig):
    name = 'cases'
