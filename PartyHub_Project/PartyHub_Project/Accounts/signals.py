from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from PartyHub_Project.Accounts.models import UserProfile


# Сигнал за създаване на профил след създаването на потребител
@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:  # Това означава, че потребителят е създаден
        UserProfile.objects.create(user=instance,)

# Сигнал за запазване на профил при всяка промяна на потребителя
@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()