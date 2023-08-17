from django.apps import AppConfig

class SimilarityCheckerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'similarity_checker'

    def ready(self):
        import similarity_checker.signals
