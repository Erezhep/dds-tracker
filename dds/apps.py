from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_inital_data(sender, **kwargs):
    from .models import TransactionType, Status
    
    TransactionType.objects.get_or_create(name="Пополнение")
    TransactionType.objects.get_or_create(name="Списание")

    Status.objects.get_or_create(name="Бизнес")
    Status.objects.get_or_create(name="Личное")
    Status.objects.get_or_create(name="Налог")


class DdsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dds'

    def ready(self):
        post_migrate.connect(create_inital_data, sender=self)