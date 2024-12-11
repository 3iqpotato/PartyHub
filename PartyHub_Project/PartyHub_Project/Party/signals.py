from django.db.models.signals import post_delete
from django.dispatch import receiver
from cloudinary.uploader import destroy
from PartyHub_Project.Party.models import Party


@receiver(post_delete, sender=Party)
def delete_party_picture(sender, instance, **kwargs):
    # Проверка дали обектът има снимка
    if instance.picture:
        # Изтриване на снимката от Cloudinary
        destroy(instance.picture.public_id)