from django.apps import AppConfig


class PortfolioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'portfolio'
    verbose_name = 'Ajagare Rahul Portfolio'
    
    def ready(self):
        """
        Import signals when the app is ready
        """
        import portfolio.signals  # noqa
