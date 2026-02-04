from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import ChatProfile

@receiver(post_save, sender=User)
def create_user_chatprofile(sender, instance, created, **kwargs):
    if created:
        ChatProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_chatprofile(sender, instance, **kwargs):
    instance.chat_profile.save()