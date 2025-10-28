from django.apps import AppConfig

class ReviewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reviews'

    def ready(self):
        from django.contrib import admin
        admin.site.enable_nav_sidebar = False
