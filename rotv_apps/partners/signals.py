from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from .models import MediaPatronage


@receiver(pre_save, sender=MediaPatronage)
def pre_save_media_patronage(sender, instance, raw, **kwargs):
    if instance.pk:
        original = sender.objects.get(pk=instance.pk)
        if instance.active and not original.active:
            instance.activated = timezone.now()
